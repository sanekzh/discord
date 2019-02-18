from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic import View

from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from .models import SiteSettings, SALES_AGENT


# def index(request):
#     return render(request, "announceusio/index.html")

def index(request):
    """ Here we are displaying index page."""
    settings = SiteSettings.objects.first()

    # What you want the button to do.
    paypal_dict = {
        "business": settings.paypal_email,
        "amount": settings.price,
        "item_name": settings.item_name,
        "invoice": "{}".format(str(uuid.uuid4())),
        "notify_url": "https://announceus.io" + reverse('paypal-ipn'),
        "return": "https://announceus.io" + reverse('announceusio:index'),
        "cancel_return": "https://announceus.io" + reverse('announceusio:index'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "announceusio/index.html", context)

def renew(request):
    settings = SiteSettings.objects.first()

    paypal_dict = {
        "business": settings.paypal_email,
        "amount": settings.price,
        "item_name": settings.item_name,
        "invoice": "{}".format(str(uuid.uuid4())),
        "notify_url": "https://announceus.io" + reverse('paypal-ipn'),
        "return": "https://announceus.io" + reverse('index'),
        "cancel_return": "https://announceus.io" + reverse('index'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }


    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "announceusio/renew.html", context)


def payment(request):
    """ Here we are displaying index page."""
    settings = SiteSettings.objects.first()

    # What you want the button to do.
    paypal_dict = {
        "business": settings.paypal_email,
        "amount": settings.price,
        "item_name": settings.item_name,
        "invoice": "{}".format(str(uuid.uuid4())),
        "notify_url": "http://announceus.io" + reverse('paypal-ipn'),
        "return": "https://announceus.io" + reverse('index'),
        "cancel_return": "https://announceus.io" + reverse('index'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "announceusio/payment.html", context)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy('announceusio:dashboard')

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutFormView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('announceusio:index'))

class Dashboard(View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = {'menu': 'Dashboard'}
            return render(request, self.template_name, data)
        return render(request, reverse_lazy('announceusio:index'), {'error': False})
        # if request.user.in_group(SALES_AGENT):
        #     return HttpResponseRedirect(reverse('core:manage_clients'))
        # if request.user:
        #     return HttpResponseRedirect(reverse(self.second_template_name))


class Members(View):
    template_name = 'dashboard/members.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = {'menu': 'Members'}
            return render(request, self.template_name, data)
        return render(request, reverse_lazy('announceusio:index'), {'error': False})


class BotMessages(View):
    template_name = 'dashboard/bot_messages.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = {'menu': 'Bot messages'}
            return render(request, self.template_name, data)
        return render(request, reverse_lazy('announceusio:index'), {'error': False})


class UserSettings(View):
    template_name = 'dashboard/user_settings.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = {'menu': 'User settings'}
            return render(request, self.template_name, data)
        return render(request, reverse_lazy('announceusio:index'), {'error': False})


class Billing(View):
    template_name = 'dashboard/billing.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data = {'menu': 'Billing'}
            return render(request, self.template_name, data)
        return render(request, reverse_lazy('announceusio:index'), {'error': False})

