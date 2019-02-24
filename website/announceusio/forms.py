from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm

from .models import Member, SiteSettings


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ('discord_username', 'discord_id', 'email', 'subscription_date_expire',
                  'notify_7', 'notify_3', 'notify_24h', 'is_invited', 'is_activated')

    discord_username = forms.CharField(max_length=200, required=True)
    discord_id = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(max_length=200, required=True)
    subscription_date_expire = forms.DateTimeField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    notify_7 = forms.BooleanField(required=False)
    notify_3 = forms.BooleanField(required=False)
    notify_24h = forms.BooleanField(required=False)
    is_invited = forms.BooleanField(required=False)
    is_activated = forms.BooleanField(required=False)


class BotSettingsForm(ModelForm):
    class Meta:
        model = SiteSettings
        fields = ('price', 'item_name', 'paypal_email', 'email', 'email_password',
                  'discord_channel_id', 'discord_server_id', 'bot_token', 'sub_days',
                  'member_role', 'message_body')

    price = forms.CharField(max_length=20, required=True)
    item_name = forms.CharField(max_length=255, required=True)
    paypal_email = forms.EmailField(max_length=300, required=True)
    email = forms.EmailField(max_length=300, required=True)
    email_password = forms.CharField(max_length=255, required=True)
    discord_channel_id = forms.CharField(max_length=255, required=True)
    discord_server_id = forms.CharField(required=True)
    bot_token = forms.CharField(max_length=255, required=True)
    sub_days = forms.IntegerField(required=True)
    member_role = forms.CharField(max_length=255, required=True)
    message_body = forms.CharField(widget=forms.Textarea, required=True)
