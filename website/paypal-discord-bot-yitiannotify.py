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
from announceusio.models import Member, SiteSettings, BotSettings, EmailSettings, Billing, BotMessage
import discord
import datetime
import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

OWNER_ID = 27

client = discord.Client()
settings = BotSettings.objects.get(user_id=OWNER_ID)
bot_message = BotMessage.objects.get(user_id=OWNER_ID)

def renew_membership(discord_id):
    """ Here we are generating paypal transaction link
        using it user will buy membership."""

    member = Member.objects.filter(user_id=OWNER_ID, discord_id=discord_id).first()
    if member:
        # message = "Renewal link http://announceus.io/renew/?email={}".format(member.email)
        message = str(bot_message.renewal_link).format(member.email)
    else:
        # message = "Please buy membership http://announceus.io"
        message = bot_message.buy_membership

    return message


def get_status(discord_id):
    """ Here we are checking in database user status
        how many days he/she has left before their membership ends."""

    # Getting from database member
    member = Member.objects.filter(user_id=OWNER_ID, discord_id=discord_id).first()

    # Checking if member does exists.
    if member:
        # calculating days left
        days_left = member.subscription_date_expire - datetime.datetime.now(
            datetime.timezone.utc)

        # subscripting for fancy look delta time
        days_left = str(days_left)[:-10]

        # message = "You have {} hours left before expiration!".format(days_left)
        message = str(bot_message.before_expiration).format(days_left)
    else:
        # message = "You should activate your membership with command !activate example@example.com"
        message = str(bot_message.should_activate)

    return message

def help_message():
        # help_message = """
        # ``` Supported commands:
        # !activate example@example.com - you activate your membershp.
        # !renew - you get membership renewal link.
        # !status - gives days left before expiration.
        # !help - show help message.
        # ```
        #
        # """
        help_message = bot_message.help_message_body
        return help_message

def embed_message(title, description):
    text = discord.Embed(title=title, description=description, color=0x41BEFB)
    text.set_footer(text="YitianNotify.com | by © CookStrt.io", icon_url="https://pbs.twimg.com/profile_images/1101004799082926082/f1rDA6a2_400x400.jpg")
    return text

def activate_user(author, email):
    """ We here are activating user email address."""

    message = None
    activate = True
    member = Member.objects.filter(user_id=OWNER_ID).filter(Q(email=email) | Q(discord_id=author.id)).first()
    if member.subscription_date_expire:
        time_left = member.subscription_date_expire - datetime.datetime.now(datetime.timezone.utc)
        if time_left.days > 0:
            activate = True
        else:
            activate = False
    else:
        activate = True
    # Checking if user is trying to use different email...
    if member and member.email.lower() != email.lower():
        # message = "This is not your email. You have been activated with a different email."
        message = bot_message.wrong_email
        return False, message

    # checking if memebr exists and already is activated.
    elif member and member.is_activated and member.discord_id == author.id:
        # message = "You are already activated! " + get_status(author.id)
        message = bot_message.already_activated + get_status(author.id)
        return False, message

    # checking if member email is presents in database but is not activated.
    # this means he/she got paid but not yet activated.

    elif member and member.is_activated == False and activate:

        # Discord username like user#1234
        member.discord_username = author

        # Assign discord user id
        member.discord_id = author.id

        # Adding days
        billing_settings = Billing.objects.filter(user_id=OWNER_ID).first()
        days = billing_settings.sub_days if billing_settings.sub_days else 30
        member.subscription_date_expire = datetime.datetime.now() + datetime.timedelta(days=days)

        # Set activated status true.
        member.is_activated = True
        # Saving in database.
        member.save()

        # message = "You have been activated! {}".format(get_status(author.id))
        message = str(bot_message.activated).format(get_status(author.id))
        print("I amin activation", message)

        return True, message

    else:
        # message = "You can buy a membership on http://announceus.io"
        message = bot_message.buy_membership
        return False, message



async def member_invite():
    """ This function is a task.
    We here are checking database for emails
    which are not yet invited. We invite them
    by sending email to them with discord link.
    """
    await client.wait_until_ready()
    while not client.is_closed:

        members = Member.objects.filter(user_id=OWNER_ID, is_invited=False)
        if members:
            # settings = SiteSettings.objects.first()
            email_settings = EmailSettings.objects.filter(user_id=OWNER_ID).first()
            email_owner = email_settings.email.lower()
            bot_settings = BotSettings.objects.filter(user_id=OWNER_ID).first()
            smtp_client = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_client.ehlo()
            smtp_client.starttls()
            smtp_client.login(email_owner, email_settings.email_password)
            for member in members:
                invite = await client.create_invite(destination=client.get_channel(bot_settings.discord_channel_id), max_uses=1)
                message_text = email_settings.message_body.format(invite_url=invite.url)
                message_body = MIMEText(message_text)
                message = MIMEMultipart()
                message['From'] = email_owner
                message['To'] = member.email.lower()
                message['Subject'] = email_settings.email_subject
                message.attach(message_body)
                smtp_client.sendmail(email_owner,
                                     member.email.lower(), message.as_string())
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
        members = Member.objects.filter(user_id=OWNER_ID, is_activated=True, discord_id__isnull=False)
        #members = members.exclude(discord_id__isnull=True)
        for member in members:
            # Getting user in the server. Connecting to each other.
            # server = client.get_server("531541056185958421")
            # settings = SiteSettings.objects.first()
            bot_settings = BotSettings.objects.filter(user_id=OWNER_ID).first()
            server = client.get_server(bot_settings.discord_server_id)
            user = server.get_member(member.discord_id)
            time_left = member.subscription_date_expire - datetime.datetime.now(datetime.timezone.utc)
            if member.notify_7 is False and time_left.days <= 7 and time_left.seconds == 0:
                print("7 days", member)
                member.notify_7 = True
                member.save()
                # await client.send_message(user, embed=embed_message("Reminder", "Hello {}, This is your 1st reminder that your Premium Membership expires in 7 days. To renew your membership use !renew command.".format(member.discord_username)))
                await client.send_message(user, embed=embed_message("Reminder", str(bot_message.first_reminder).format(member.discord_username)))

            elif member.notify_3 is False and time_left.days <= 3 and time_left.seconds == 0:
                print("3 days", member)
                member.notify_3 = True
                member.save()
                # await client.send_message(user, embed=embed_message("Reminder", "Hello {}, This is your 2nd reminder that your Premium Membership expires in 3 days. To renew your membership use !renew command.".format(member.discord_username)))
                await client.send_message(user, embed=embed_message("Reminder", str(bot_message.second_reminder).format(member.discord_username)))

            # 24 hours = 86400 seconds. If I choose 1 day it will triger
            # reminder at 1 day and 23:59.
            # elif member.notify_24h is False and time_left.seconds == 86400:
            elif member.notify_24h is False and time_left.days == 1 and time_left.seconds == 0:
                print("24 hours", member)
                member.notify_24h = True
                member.save()
                # await client.send_message(user, embed=embed_message("Reminder", "Hello {}, This is your Final Reminder your membership expires in 24 hours. To renew your membership use !renew command.".format(member.discord_username)))
                await client.send_message(user, embed=embed_message("Reminder", str(bot_message.finely_reminder).format(
                                                                    member.discord_username)))

            elif member.is_activated and time_left.days <= 0:
                print(time_left.seconds)
                member.notify_3 = False
                member.notify_7 = False
                member.notify_24h = False
                member.is_activated = False

                member.save()
                print("Expired", member)

                # Removing `Member` role from expired user.
                # settings = SiteSettings.objects.first()
                role = discord.utils.get(server.roles, name=bot_settings.member_role)
                await client.remove_roles(user, role)

                # await client.send_message(user, embed=embed_message("Hello {}, Your subscription has now been expired if you wish to still renew please proceed to http://announceus.io".format(member.discord_username)))
                await client.send_message(user, embed=embed_message("Reminder", str(bot_message.expired_reminder).format(member.discord_username)))


        await asyncio.sleep(2)


@client.event
async def on_ready():
    """ This function executes when bot connects
        to the discord channel. it gives notification about it."""

    print("Bot has connected to server as {}".format(client.user))


@client.event
async def on_member_join(member):
    # await client.send_message(member,
    #                           embed=embed_message("Welcome", """Hello, {} Welcome to announceus.io discord server. Please use following Commands:
    #                           {}
    #                           """.format(member, help_message())))
    await client.send_message(member,
                              embed=embed_message("Welcome", str(bot_message.join_message).format(member, help_message())))


@client.event
async def on_message(message):
    """ Here we handle messages in channel and in private
        message to bot. Commands are we except !status and !renew. """


    if message.content.lower().startswith("!activate"):
        # we here activate user subscription!

        # parsing message for finding email address entered by user.
        email = re.search(r'[\w\.-]+@[\w\.-]+', message.content.lower())

        if email:
            print("I am here")
            activate_status = activate_user(message.author, email.group(0))
            answer = activate_status[1]
            print("if email", answer)
            if activate_status[0]:

                # settings = SiteSettings.objects.first()
                bot_settings = BotSettings.objects.filter(user_id=OWNER_ID).first()
                server = client.get_server(bot_settings.discord_server_id)
                user = server.get_member(message.author.id)
                role = discord.utils.get(server.roles, name=bot_settings.member_role)
                await client.add_roles(user, role)
        else:
            answer = "For activation please provide email address which where used for payment!"

        print(answer)
        await client.send_message(message.author, embed=embed_message("Status", answer))

    elif "!status" == message.content.lower():

        # we replay to user the status of his subscription.
        await client.send_message(message.author, embed=embed_message("Status", get_status(message.author.id)))


    elif "!renew" == message.content.lower():

        # we here reply to user the paypal link to finish transaction.
        await client.send_message(message.author, embed=embed_message("Renew", renew_membership(message.author.id)))
    elif "!help" == message.content.lower():
        await client.send_message(message.author, embed=embed_message("Help", help_message()))



# Registering member reminder task
client.loop.create_task(member_reminder())

# Registering member invite task
client.loop.create_task(member_invite())

# Running our crazy bot
# client.run("NTMxODk5NjY4NDM1Njk3NzA0.DxUqGg.S0om0c6N0eEZz6pA3xWuGKG5xlg")
client.run(settings.bot_token)
