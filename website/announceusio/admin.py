from django.contrib import admin

from .models import Member, SiteSettings


@admin.register(Member)
class AdminMember(admin.ModelAdmin):
    list_display = ("email", "discord_username", "discord_id",
                    "subscription_date_expire", "created_on")


@admin.register(SiteSettings)
class AdminSiteSettings(admin.ModelAdmin):
    list_display = ("price", "item_name", "sub_days", "member_role", "paypal_email", "email", "discord_channel_id",
                    "discord_server_id")

