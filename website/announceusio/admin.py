from django.contrib import admin

from .models import Member

@admin.register(Member)
class Member(admin.ModelAdmin):
    list_display = ("email", "discord_id",
                    "subscription_date_expire", "created_on")
