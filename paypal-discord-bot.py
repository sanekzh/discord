#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8



# id 531899668435697704
# token NTMxODk5NjY4NDM1Njk3NzA0.DxUqGg.S0om0c6N0eEZz6pA3xWuGKG5xlg
# permission 268511296
# auth url https://discordapp.com/oauth2/authorize?client_id={531899668435697704}&scope=bot&permissions={268511296}
import re
import discord

client = discord.Client()

def generate_paypal_link():
    """ Here we are generating paypal transaction link
        using it user will buy membership."""


    return "http://paypal.com"


def get_status():
    """ Here we are checking in database user status
        how many days he/she has left before their membership ends."""

    return "You have 3 days left before expire!"


def activate_user(email):
    """ We here are activating user email address."""

    return "Your subscription has been activated with email - {}".format(email)




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


    print(message.channel, message.author, message.author.name, message.content)
    user_info = client.get_user_info(message.author.id)




    if message.content.lower().startswith("!activate"):
        # we here activate user subscription!

        # parsing message for finding email address entered by user.
        email = re.search(r'[\w\.-]+@[\w\.-]+', message.content.lower())

        if email:
            answer = activate_user(email.group(0))
        else:
            answer = "For activation please provide email address which where used for payment!"

        await client.send_message(message.author, answer)

    elif "!status" == message.content.lower():

        # we replay to user the status of his subscription.
        await client.send_message(message.author, get_status())


    elif "!renew" == message.content.lower():

        # we here reply to user the paypal link to finish transaction.
        await client.send_message(message.author, generate_paypal_link())



client.run("NTMxODk5NjY4NDM1Njk3NzA0.DxUqGg.S0om0c6N0eEZz6pA3xWuGKG5xlg")
