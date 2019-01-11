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

from announceusio.models import Member

import discord
import datetime


client = discord.Client()



def renew_membership(discord_id):
    """ Here we are generating paypal transaction link
        using it user will buy membership."""

    member = Member.objects.filter(discord_id=discord_id).first()
    if member:
        message = "You can renew your membership the using following link http://announceus.io/renew/?email={}".format(member.email)

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

        message = "You have {} hours left before expire!".format(days_left)
    else:
        message = "You should activate your membership with command !activate example@example.com"

    return message




def activate_user(author, email):
    """ We here are activating user email address."""

    message = None
    member = Member.objects.filter(Q(email=email) | Q(discord_id=author.id)).first()

    # checking if memebr exists and already is activated.
    if member and member.is_activated and member.discord_id == author.id:
        message = "You have been already activated! " + get_status(author.id)
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
        message = "This is not your email. You have been activated with different email."
        return False, message
    else:
        message = "You should buy membership on http://announceus.io"
        return False, message





@client.event
async def on_ready():
    """ This function executes when bot connects
        to the discord channel. it gives notification about it."""

    print("Bot has connected to server as {}".format(client.user))


@client.event
async def on_member_join(member):
    await client.send_message(member, "Hello, {} Welcome to Testing server," +
                              "Please use following Commands" +
                              " !activate your@email.com," +
                              " !status and !renew.".format(member))


@client.event
async def on_message(message):
    """ Here we handle messages in channel and in private
        message to bot. Commands are we except !status and !renew. """


    # print(message.channel, message.author, message.author.name, message.content)


    if message.content.lower().startswith("!activate"):
        # we here activate user subscription!

        # parsing message for finding email address entered by user.
        email = re.search(r'[\w\.-]+@[\w\.-]+', message.content.lower())

        if email:
            activate_status = activate_user(message.author, email.group(0))
            answer = activate_status[1]
            if activate_status[0]:

                server = client.get_server("531541056185958421")
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



client.run("NTMxODk5NjY4NDM1Njk3NzA0.DxUqGg.S0om0c6N0eEZz6pA3xWuGKG5xlg")
