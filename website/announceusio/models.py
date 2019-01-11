from django.db import models

from paypal.standard.ipn.signals import valid_ipn_received

import datetime


class Member(models.Model):
    """
    This is member class for members.
    we are here saving data about our premium users.
    email - the mail which is provided by paypal.
            we save it to database when ipn success
            signal is received. After that we are
            waiting for user to activate their account
            from discord.

    discord_username - we assign here discord username
                       when user uses !activate command
                       in our discord channel.

    discord_id - the user's discord id. Its an integer
                 assigned to user by discord.

    subscription_date_expire - the date when premium member
                                subscription will expire.
                                We are depending on this table
                                to calculate how much days
                                has left user.

    notify_7, notify_3, notify_24h - this tables are used
                                     to control the notification
                                     of to remind users to renew
                                     their membership.
                                     We check if we already have
                                     to sent the reminder. We do
                                     not want to spam users.

    is_activated - this table shows us if user is activated or
                    disabled. True or False.

    created_on - the date when made record to database.
    """

    email = models.EmailField(max_length=300, blank=True,
                              null=True, unique=True)
    discord_username = models.CharField(max_length=300, blank=True,
                                        null=True, unique=True)
    discord_id = models.IntegerField(blank=True, null=True, unique=True)

    subscription_date_expire = models.DateTimeField(blank=True, null=True)

    notify_7 = models.BooleanField(default=False)
    notify_3 = models.BooleanField(default=False)
    notify_24h = models.BooleanField(default=False)

    is_activated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.email, self.discord_id,
                                 self.subscription_date_expire)



def payment_received_succes(sender, **kwargs):
    """ This is callback handler for valid_ipn_received signal.

    We are here checking whether payer_email is already
    in database or not. We are creating members here after
    transaction was successfully.
    """

    ipn_obj = sender

    member = Member.objects.filter(email=ipn_obj.payer_email).get()
    print(member)

    if member:
        # If the user already exists in database we are just adding 30
        # days to her/him.
        member.subscription_date_expire = member.subscription_date_expire + datetime.timedelta(days=30)

        member.notify_7 = False
        member.notify_3 = False
        member.notify_24h = False

        member.save()
    else:
        new_member = Member(
            email=ipn_obj.payer_email)

        new_member.save()

        print("I have saved it!")

    print("HERE IS EMAIL ", member)





valid_ipn_received.connect(payment_received_succes)
