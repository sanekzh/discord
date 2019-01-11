from django.shortcuts import render
from django.http import HttpResponse

from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
import uuid



# def index(request):
#     return render(request, "announceusio/index.html")

def index(request):
    """ Here we are displaying index page."""
    print(reverse('paypal-ipn'))
    print(request.get_host())

    # What you want the button to do.
    paypal_dict = {
        "business": "beradze@europe.com",
        "amount": "35",
        "item_name": "announceus.io - PREMIUM",
        "invoice": "{}".format(str(uuid.uuid4())),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('index')),
        "cancel_return": request.build_absolute_uri(reverse('index')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    print(dir(PayPalPaymentsForm))
    return render(request, "announceusio/index.html", context)

def renew(request):

    paypal_dict = {
        "business": "beradze@europe.com",
        "amount": "35",
        "item_name": "announceus.io - PREMIUM",
        "invoice": "{}".format(str(uuid.uuid4())),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('index')),
        "cancel_return": request.build_absolute_uri(reverse('index')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "announceusio/renew.html", context)
