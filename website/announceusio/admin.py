from django.contrib import admin

from .models import Member, SiteSettings, BotSettings, EmailSettings, Billing, BotMessage, UserProfile, Stripe


@admin.register(Member)
class AdminMember(admin.ModelAdmin):
    list_display = ("email", "discord_username", "discord_id",
                    "subscription_date_expire", "created_on")


@admin.register(SiteSettings)
class AdminSiteSettings(admin.ModelAdmin):
    list_display = ("price", "item_name", "sub_days", "member_role", "paypal_email", "email", "discord_channel_id",
                    "discord_server_id")


@admin.register(BotSettings)
class AdminBotSettings(admin.ModelAdmin):
    list_display = ("user", "discord_channel_id", "discord_server_id", "bot_token", "member_role")


@admin.register(EmailSettings)
class AdminEmailSettings(admin.ModelAdmin):
    list_display = ("user", "email", "email_password", "message_body")


@admin.register(Billing)
class AdminBilling(admin.ModelAdmin):
    list_display = ("user", "price", "sub_days", "item_name", "paypal_email")


@admin.register(BotMessage)
class AdminBotMessage(admin.ModelAdmin):
    list_display = ("user",  'help_message_body', 'wrong_email', 'already_activated', 'activated', 'before_expiration',
                    'should_activate', 'renewal_link', 'buy_membership')


@admin.register(UserProfile)
class AdminUserProfile(admin.ModelAdmin):
    list_display = ("user",  'company')


@admin.register(Stripe)
class AdminStripe(admin.ModelAdmin):
    list_display = ("amount", "id_transaction", "status", "payer_email", "created_on")
