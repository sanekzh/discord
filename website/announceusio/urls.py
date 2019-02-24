#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

app_name = 'announceusio'

urlpatterns = [
    path("", views.index, name="index"),
    path("renew/", views.renew, name="renew"),
    path("payment/", views.payment, name="payment"),
    path("dashboard/", views.LoginFormView.as_view(), name='login'),
    path("logout/", views.LogoutFormView.as_view(), name='logout'),
    path("dashboard_show/", login_required()(views.Dashboard.as_view()), name="dashboard"),
    path("members/", login_required()(views.Members.as_view()), name="members"),
    path("add_member/", login_required()(views.AddMember.as_view()), name="add_member"),
    path("bot_messages/", login_required()(views.BotMessages.as_view()), name="bot_messages"),
    path("bot_settings/", login_required()(views.BotSettings.as_view()), name="bot_settings"),
    path("user_settings/", login_required()(views.UserSettings.as_view()), name="user_settings"),
    path("billing/", login_required()(views.Billing.as_view()), name="billing"),

]
