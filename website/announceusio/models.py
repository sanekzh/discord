import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User

from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received


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

    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    email = models.EmailField(max_length=200, blank=True,
                              null=True, unique=True)
    discord_username = models.CharField(max_length=200, blank=True,
                                        null=True, unique=True)
    discord_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    subscription_date_expire = models.DateTimeField(blank=True, null=True)

    notify_7 = models.BooleanField(default=False)
    notify_3 = models.BooleanField(default=False)
    notify_24h = models.BooleanField(default=False)

    is_invited = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    # Would be great to make another child table to this one
    # and move there all notification column staff.

    def __str__(self):
        return "{} {} {}".format(self.email, self.discord_id,
                                 self.subscription_date_expire)


class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, unique=True)
    price = models.CharField(default="25", max_length=20, blank=False, null=False)
    sub_days = models.IntegerField(default=30, blank=False, null=False)
    item_name = models.CharField(default="announceus.io - PREMIUM", max_length=255, blank=False, null=False)
    paypal_email = models.EmailField(max_length=300, default="some@mail.com", blank=False, null=False)


class BotSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, unique=True)
    discord_channel_id = models.CharField(max_length=255, blank=False, null=False)
    discord_server_id = models.CharField(default="asds", max_length=255, blank=False, null=False)
    bot_token = models.CharField(max_length=255, blank=False, null=False)
    member_role = models.CharField(default="Member", max_length=255, blank=False, null=False)


class EmailSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, unique=True)
    message_body = models.TextField(default="{invite_url}", help_text="You must set {invite_url} in message body!",
                                    blank=False, null=False)
    email = models.EmailField(max_length=300, blank=False, null=False)
    email_password = models.CharField(max_length=255, blank=False, null=False)


HELP_MESSAGE = """```Supported commands:

!activate example@example.com - you activate your membershp.

!renew - you get membership renewal link.

!status - gives days left before expiration.

!help - show help message.
```"""
WRONG_EMAIl = "This is not your email. You have been activated with a different email."
ALREADY_ACTIVATED = "You are already activated! "
ACTIVATED = "You have been activated! {}"
BEFORE_EXPIRATION = "You have {} hours left before expiration!"
SHOULD_ACTIVATE = "You should activate your membership with command !activate example@example.com"
RENEW_LINK = "Renewal link http://announceus.io/renew/?email={}"
BUY_MEMBERSHIP = "Please buy membership http://announceus.io"


class BotMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, unique=True)
    # !help
    help_message_body = models.TextField(default=HELP_MESSAGE, blank=False, null=False)
    # !activate
    wrong_email = models.TextField(default=WRONG_EMAIl, blank=False, null=False)
    already_activated = models.TextField(default=ALREADY_ACTIVATED, blank=False, null=False)
    activated = models.TextField(default=ACTIVATED, blank=False, null=False)
    # !status
    before_expiration = models.TextField(default=BEFORE_EXPIRATION, blank=False, null=False)
    should_activate = models.TextField(default=SHOULD_ACTIVATE, blank=False, null=False)
    # !renew
    renewal_link = models.TextField(default=RENEW_LINK, blank=False, null=False)
    buy_membership = models.TextField(default=BUY_MEMBERSHIP, blank=False, null=False)


class SiteSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, unique=True)
    price = models.CharField(default="25", max_length=20, blank=False,
                                null=False)

    item_name = models.CharField(default="announceus.io - PREMIUM",
                                 max_length=255, blank=False, null=False)

    paypal_email = models.EmailField(max_length=300,
                                     default="some@mail.com",
                                     blank=False, null=False)

    email = models.EmailField(max_length=300, blank=False,
                              null=False)

    email_password = models.CharField(max_length=255, blank=False,
                                      null=False)

    discord_channel_id = models.CharField(max_length=255, blank=False,
                                  null=False)

    discord_server_id = models.CharField(default="asds", max_length=255, blank=False,
                                         null=False)

    bot_token = models.CharField(max_length=255, blank=False,
                                 null=False)

    sub_days = models.IntegerField(default=30, blank=False, null=False)

    member_role = models.CharField(default="Member", max_length=255, blank=False, null=False)

    message_body = models.TextField(default="{invite_url}", help_text="You must set {invite_url} in message body!", blank=False, null=False)


    def __str__(self):
        return "{} {} {}".format(self.price, self.item_name, self.email)


def payment_received_succes(sender, **kwargs):
    """ This is callback handler for valid_ipn_received signal.

    We are here checking whether payer_email is already
    in database or not. We are creating members here after
    transaction was successfully.
    """

    ipn_obj = sender

    member = Member.objects.filter(email=ipn_obj.payer_email).exists()
    settings = SiteSettings.objects.first()
    print("I am in valid ipn")
    print(ipn_obj)


    if member:
        print("I am here...")
        # If the user already exists in database we are just adding 30
        # days to her/him.
        member = Member.objects.filter(email=ipn_obj.payer_email).first()
        if member.subscription_date_expire is not None:
            member.subscription_date_expire = member.subscription_date_expire + datetime.timedelta(days=settings.sub_days)
        else:
            member.subscription_date_expire = datetime.datetime.now() + datetime.timedelta(days=settings.sub_days)


        is_activated = True
        member.notify_7 = False
        member.notify_3 = False
        member.notify_24h = False

        member.save()
    else:
        # Saving starting point of Member.
        new_member = Member(email=ipn_obj.payer_email)
        new_member.save()




def invalid_payment(sender, **kwargs):
    print("I am here in invalid payment")
    print(sender)

invalid_ipn_received.connect(invalid_payment)
valid_ipn_received.connect(payment_received_succes)
