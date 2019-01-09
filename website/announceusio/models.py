from django.db import models


class Member(models.Model):
    email = models.EmailField(max_length=300, blank=True,
                              null=True, unique=True)
    discord_username = models.CharField(max_length=300, blank=True,
                                        null=True, unique=True)
    discord_id = models.IntegerField(blank=True, null=True, unique=True)
    subscription_date_expire = models.DateTimeField(blank=True, null=True)
    notify_7 = models.BooleanField(default=False)
    notify_3 = models.BooleanField(default=False)
    notify_24h = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.email, self.discord_id,
                                 self.subscription_date_expire)
