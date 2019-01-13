#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8


from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("renew/", views.renew, name="renew"),
    path("payment/", views.payment, name="payment")
]
