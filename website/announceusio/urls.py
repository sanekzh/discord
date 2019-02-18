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
    # path('dashboard/', TemplateView.as_view(template_name='login.html'), name='login'),
    re_path("dashboard_show/.*", login_required()(views.Dashboard.as_view()), name="dashboard")
]
