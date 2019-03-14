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
    path("dashboard_show/", login_required()(views.DashboardView.as_view()), name="dashboard"),
    path("owner/", login_required()(views.OwnerView.as_view()), name="owner"),
    path("members/", login_required()(views.MembersView.as_view()), name="members"),
    path("add_member/", login_required()(views.AddMemberView.as_view()), name="add_member"),
    path("member_update/", login_required()(views.MembersView.as_view()), name="members"),
    path("bot_messages/", login_required()(views.BotMessagesView.as_view()), name="bot_messages"),
    path("bot_settings/", login_required()(views.BotSettingsView.as_view()), name="bot_settings"),
    path("email_settings/", login_required()(views.EmailSettingsView.as_view()), name="email_settings"),
    path("user_settings/", login_required()(views.UserSettingsView.as_view()), name="user_settings"),
    path("billing/", login_required()(views.BillingSettingsView.as_view()), name="billing"),
    path("bot_status/", login_required()(views.BotStatusView.as_view()), name="bot_status"),
    path("paypal_page/", login_required()(views.PayPalIPNView.as_view()), name="paypal_page"),
    path("paypal_table/", login_required()(views.PayPalTableView.as_view()), name="paypal_table"),
    path("stripe/", login_required()(views.StripeView.as_view()), name="stripe"),
]
