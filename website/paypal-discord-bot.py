#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

# id 531899668435697704
# token NTMxODk5NjY4NDM1Njk3NzA0.DxUqGg.S0om0c6N0eEZz6pA3xWuGKG5xlg
# permission 268511296
# auth url https://discordapp.com/oauth2/authorize?client_id={531899668435697704}&scope=bot&permissions={268511296}
import re
import os
import django
from django.db.models import Q
os.environ["DJANGO_SETTINGS_MODULE"] = "website.settings"
django.setup()
from announceusio.models import Member, Invite, SiteSettings
import discord
import datetime
import asyncio
import smtplib


client = discord.Client()
settings = SiteSettings.objects.first()

def renew_membership(discord_id):
    """ Here we are generating paypal transaction link
        using it user will buy membership."""

    member = Member.objects.filter(discord_id=discord_id).first()
    if member:
        message = "Renewal link http://announceus.io/renew/?email={}".format(member.email)
    else:
        message = "Please buy membership http://announceus.io"

    return message


def get_status(discord_id):
    """ Here we are checking in database user status
        how many days he/she has left before their membership ends."""

    # Getting from database member
    member = Member.objects.filter(discord_id=discord_id).first()

    # Checking if member does exists.
    if member:
        # calculating days left
        days_left = member.subscription_date_expire - datetime.datetime.now(
            datetime.timezone.utc)

        # subscripting for fancy look delta time
        days_left = str(days_left)[:-10]

        message = "You have {} hours left before expiration!".format(days_left)
    else:
        message = "You should activate your membership with command !activate example@example.com"

    return message

def help_message():
        help_message = """
        ``` Supported commands:
        !activate example@example.com - you activate your membershp.
        !renew - you get membership renewal link.
        !status - gives days left before expiration.
        !help - show help message.
        ```

        """
        return help_message


def activate_user(author, email):
    """ We here are activating user email address."""

    message = None
    member = Member.objects.filter(Q(email=email) | Q(discord_id=author.id)).first()

    # checking if memebr exists and already is activated.
    if member and member.is_activated and member.discord_id == author.id:
        message = "You are already activated! " + get_status(author.id)
        return False, message

    # checking if member email is presents in database but is not activated.
    # this means he/she got paid but not yet activated.
    elif member and member.is_activated == False:

        # Discord username like user#1234
        member.discord_username = author

        # Assign discord user id
        member.discord_id = author.id

        # Adding days
        member.subscription_date_expire = datetime.datetime.now() + datetime.timedelta(days=30)

        # Set activated status true.
        member.is_activated = True
        # Saving in database.
        member.save()

        message = "You have been activated! {}".format(get_status(author.id))

        return True, message

    # Checking if user is trying to use different email...
    elif member and member.email != email:
        message = "This is not your email. You have been activated with a different email."
        return False, message
    else:
        message = "You can buy a membership on http://announceus.io"
        return False, message

async def member_invite():
    """ This function is a task.
    We here are checking database for emails
    which are not yet invited. We invite them
    by sending email to them with discord link.
    """
    await client.wait_until_ready()
    while not client.is_closed:

        members = Invite.objects.filter(is_invited=False).all()
        if members:
            smtp_client = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_client.starttls()
            smtp_client.login(settings.email, settings.email_password)
            for member in members:
                invite = await client.create_invite(destination=client.get_channel(settings.discord_channel_id), max_uses=1)
                message = """From:  Announceus.io Invite <{}>
                To:  <{}>
                Subject:  <Announceus.io Invite>\n\n

                Hello,

                 Thank you for join ANNOUNCEUS.IO

                 Please follow the following Steps:

                     1. Join Our Discord > > {}

                     2. Enjoy!

                     Thanks
                     ANNOUNCEUS.IO
                """.format(settings.email, member.email, invite.url)
                smtp_client.sendmail(settings.email,
                                     member.email, message)
                print(member)
                member.is_invited = True
                member.save()
        await asyncio.sleep(2)


async def member_reminder():
    """ This function is running as task.
    Here we are checking how many days has
    left and remind them to renew for additional
    days. If the time has come we remove from user
    `Member` role. Switch is_activated to False,
    Clearing the subscription_date_expire column.
    """
    await client.wait_until_ready()
    while not client.is_closed:
        members = Member.objects.filter(is_activated=True).all()
        for member in members:
            # Getting user in the server. Connecting to each other.
            # server = client.get_server("531541056185958421")
            server = client.get_server(settings.discord_server_id)
            user = server.get_member(member.discord_id)
            time_left = member.subscription_date_expire - datetime.datetime.now(datetime.timezone.utc)
            if member.notify_7 is False and time_left.days <= 7 and time_left.seconds == 0:
                print("7 days", member)
                member.notify_7 = True
                member.save()
                await client.send_message(user, "Hello {}, This is your 1st reminder that your Premium Membership expires in 7 days. To renew your membership use !renew command.".format(member.discord_username))

            elif member.notify_3 is False and time_left.days <= 3 and time_left.seconds == 0:
                print("3 days", member)
                member.notify_3 = True
                member.save()
                await client.send_message(user, "Hello {}, This is your 2nd reminder that your Premium Membership expires in 3 days. To renew your membership use !renew command.".format(member.discord_username))

            # 24 hours = 86400 seconds. If I choose 1 day it will triger
            # reminder at 1 day and 23:59.
            # elif member.notify_24h is False and time_left.seconds == 86400:
            elif member.notify_24h is False and time_left.days == 1 and time_left.seconds == 0:
                print("24 hours", member)
                member.notify_24h = True
                member.save()
                await client.send_message(user, "Hello {}, This is your Final Reminder your membership expires in 24 hours. To renew your membership use !renew command.".format(member.discord_username))
            elif member.is_activated and time_left.days <= 0:
                print(time_left.seconds)
                member.notify_3 = False
                member.notify_7 = False
                member.notify_24h = False
                member.is_activated = False

                member.save()
                print("Expired", member)

                # Removing `Member` role from expired user.
                role = discord.utils.get(server.roles, name="Member")
                await client.remove_roles(user, role)

                await client.send_message(user, "Hello {}, Your subscription has now been expired if you wish to still renew please proceed to http://announceus.io".fomat(member.discord_username))


        await asyncio.sleep(2)


@client.event
async def on_ready():
    """ This function executes when bot connects
        to the discord channel. it gives notification about it."""

    print("Bot has connected to server as {}".format(client.user))


@client.event
async def on_member_join(member):
    await client.send_message(member,
                              """Hello, {} Welcome to announceus.io discord server. Please use following Commands:
                              {}
                               """.format(member, help_message()))



@client.event
async def on_message(message):
    """ Here we handle messages in channel and in private
        message to bot. Commands are we except !status and !renew. """


    if message.content.lower().startswith("!activate"):
        # we here activate user subscription!

        # parsing message for finding email address entered by user.
        email = re.search(r'[\w\.-]+@[\w\.-]+', message.content.lower())

        if email:
            activate_status = activate_user(message.author, email.group(0))
            answer = activate_status[1]
            if activate_status[0]:

                server = client.get_server(settings.discord_server_id)
                user = server.get_member(message.author.id)
                role = discord.utils.get(server.roles, name="Member")
                await client.add_roles(user, role)
        else:
            answer = "For activation please provide email address which where used for payment!"

        await client.send_message(message.author, answer)

    elif "!status" == message.content.lower():

        # we replay to user the status of his subscription.
        await client.send_message(message.author, get_status(message.author.id))


    elif "!renew" == message.content.lower():

        # we here reply to user the paypal link to finish transaction.
        await client.send_message(message.author, renew_membership(message.author.id))
    elif "!help" == message.content.lower():
        await client.send_message(message.author, help_message())



# Registering member reminder task
client.loop.create_task(member_reminder())

# Registering member invite task
client.loop.create_task(member_invite())

# Running our crazy bot
# client.run("NTMxODk5NjY4NDM1Njk3NzA0.DxUqGg.S0om0c6N0eEZz6pA3xWuGKG5xlg")
client.run(settings.bot_token)
