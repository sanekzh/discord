import json
import os
import uuid
from shutil import copyfile

import requests
from bs4 import BeautifulSoup
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from django.http import HttpResponse, QueryDict
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import View
from django.views.generic.edit import FormView
from paypal.standard.forms import PayPalPaymentsForm, PayPalStandardBaseForm
from paypal.standard.ipn.models import PayPalIPN

from .credentials.credentials import SERVER_SUPERVISOR_URL, SERVER_SUPERVISOR_LOGIN, SERVER_SUPERVISOR_PASSWORD
from .forms import MemberForm, PayPalForm
from .models import Member, Billing, EmailSettings, BotSettings, BotMessage, UserProfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# def index(request):
#     return render(request, "announceusio/index.html")

def index(request):
    """ Here we are displaying index page."""
    user = User.objects.get(username=request.user)
    settings = Billing.objects.filter(user=user).first()
    # settings = Billing.objects.first()

    # What you want the button to do.
    paypal_dict = {
        "business": settings.paypal_email,
        "amount": settings.price,
        "item_name": settings.item_name,
        "invoice": "{}".format(str(uuid.uuid4())),
        "notify_url": "https://cookstart.io" + reverse('paypal-ipn'),
        "return": "https://cookstart.io" + reverse('announceusio:index'),
        "cancel_return": "https://cookstart.io" + reverse('announceusio:index'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "announceusio/index.html", context)


def renew(request):
    user = User.objects.get(username=request.user)
    settings = Billing.objects.filter(user=user).first()

    paypal_dict = {
        "business": settings.paypal_email,
        "amount": settings.price,
        "item_name": settings.item_name,
        "invoice": "{}".format(str(uuid.uuid4())),
        "notify_url": "https://cookstart.io" + reverse('paypal-ipn'),
        "return": "https://cookstart.io" + reverse('announceusio:index'),
        "cancel_return": "https://cookstart.io" + reverse('announceusio:index'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "announceusio/renew.html", context)


def payment(request):
    """ Here we are displaying index page."""
    user = User.objects.get(username=request.user)
    settings = Billing.objects.filter(user=user).first()

    # What you want the button to do.
    paypal_dict = {
        "business": settings.paypal_email,
        "amount": settings.price,
        "item_name": settings.item_name,
        "invoice": "{}".format(str(uuid.uuid4())),
        "notify_url": "https://cookstart.io" + reverse('paypal-ipn'),
        "return": "https://cookstart.io" + reverse('announceusio:index'),
        "cancel_return": "https://cookstart.io" + reverse('announceusio:index'),
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
        return HttpResponseRedirect(reverse('announceusio:login'))


class DashboardView(View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            status = 'unknown'
            members_active = Member.objects.filter(user=User.objects.get(username=request.user),
                                                   is_activated=True).count()
            members_all = Member.objects.filter(user=User.objects.get(username=request.user)).count()
            owner_members_email_list = Member.objects.filter(user=User.objects.get(username=request.user)).values_list('email', flat=True)
            members = Member.objects.filter(user=User.objects.get(username=request.user),
                                            discord_username__isnull=False).order_by('-id')[:10]
            user = User.objects.get(username=request.user)
            billing = Billing.objects.get(user=user)
            income = PayPalIPN.objects.filter(business=billing.paypal_email, created_at__gte=timezone.now(). \
                       replace(day=1, hour=0, minute=0, second=0, microsecond=0)).aggregate(Sum('mc_gross'))
            total_income = PayPalIPN.objects.filter(business=billing.paypal_email).aggregate(Sum('mc_gross'))
            url = f'http://{SERVER_SUPERVISOR_URL}/index.html'
            response = requests.get(url, auth=(SERVER_SUPERVISOR_LOGIN, SERVER_SUPERVISOR_PASSWORD))
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.findAll('tr')
            for tr in rows[1:]:
                cols = tr.findAll('td')
                if 'status' in cols[0]['class']:
                    state, uptime, bot, temp = [c.text for c in cols]
                    if bot == f"paypal-discord-bot-{user.username}":
                        status = state
                        break

            # income = PayPalIPN.objects. \
            #     filter(payer_email__in=list(owner_members_email_list), created_at__gte=timezone.now().
            #            replace(day=1, hour=0, minute=0, second=0, microsecond=0)).aggregate(Sum('mc_gross'))
            # total_income = PayPalIPN.objects.filter(payer_email__in=list(owner_members_email_list)).aggregate(Sum('mc_gross'))
            data = {'menu': 'Dashboard',
                    'members_active': members_active,
                    'members_all': members_all,
                    'income': income,
                    'total_income': total_income,
                    'members': members,
                    'status': status
                    }
            return render(request, self.template_name, data)
        return render(request, reverse_lazy('announceusio:login'), {'error': False})


class AddMemberView(View):
    def get(self, request, *args, **kwargs):
        try:
            ajax_response = {'sEcho': '', 'aaData': [], 'iTotalRecords': 0, 'iTotalDisplayRecords': 0}
            user = request.user
            members = Member.objects.filter(user=User.objects.get(username=request.user))
            if not members:
                return HttpResponse(json.dumps(ajax_response), content_type='application/json')
            list_name = ['discord_username', 'discord_id', 'email', 'subscription_date_expire', 'notify_7', 'notify_3',
                         'notify_24h', 'is_invited', 'is_activated']
            # search
            search = request.GET.get('search[value]', '')
            if search:
                pass
                members = members.filter(
                    Q(discord_username__icontains=search) | Q(discord_id__icontains=search)
                    | Q(email__icontains=search))
            # Sorting
            sort_column = list_name[int(request.GET.get('order[0][column]', 0))]
            if request.GET.get('order[0][dir]', None) == 'desc':
                sort_column = '-{}'.format(sort_column)
            members = members.order_by(sort_column)
            # filter
            discord_username = request.GET.get('columns[1][search][value]', False)
            discord_id = request.GET.get('columns[3][search][value]', False)
            email = request.GET.get('columns[2][search][value]', False)

            if discord_username or discord_id or email:
                members = members.filter(
                    (Q(iscord_username=discord_username) if discord_username else Q())
                    & (Q(discord_id=discord_id) if discord_id else Q())
                    & (Q(email=email) if email else Q())
                )
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            ajax_response['iTotalRecords'] = ajax_response['iTotalDisplayRecords'] = members.count()
            for member in members[start:start + length]:
                ajax_response['aaData'].append(
                    [
                        member.email,
                        member.discord_username if member.discord_username != member.email else '',
                        member.discord_id if member.discord_id != member.email else '',
                        str((member.subscription_date_expire).strftime('%B %d, %Y, %I:%M')
                            + member.subscription_date_expire.strftime(' %p').lower()) if member.subscription_date_expire else '',
                        str((member.created_on).strftime('%B %d, %Y, %I:%M') + member.created_on.strftime(' %p').lower()),
                        member.notify_7,
                        member.notify_3,
                        member.notify_24h,
                        member.is_invited,
                        member.is_activated,
                        member.id,
                        member.id
                    ])
            # json_data = serializers.serialize('json', members)
            return HttpResponse(json.dumps(ajax_response), content_type='application/json')
        except Exception as e:
            pass

    def post(self, request):
        if Member.objects.filter(user=User.objects.get(username=request.user), email=request.POST['email']).exists():
            subscription_date_expire = request.POST['subscription_date_expire']
            Member.objects.filter(email=request.POST['email']).update(
                discord_username=request.POST['discord_username'],
                discord_id=request.POST['discord_id'],
                subscription_date_expire=subscription_date_expire if subscription_date_expire else None,
                notify_7=json.loads(request.POST.get('notify_7', 'false')),
                notify_3=json.loads(request.POST.get('notify_3', 'false')),
                notify_24h=json.loads(request.POST.get('notify_24h', 'false')),
                is_invited=json.loads(request.POST.get('is_invited', 'false')),
                is_activated=json.loads(request.POST.get('is_activated', 'false'))
            )
            return HttpResponse(json.dumps({'status': 'OK'}), content_type='application/json')
        # elif Member.objects.filter(email=request.POST['email']).exists():
        #     return HttpResponse(json.dumps({'status': 'NO', 'errors': 'This email exists'}),
        #                         content_type='application/json')
        form = MemberForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            member = Member(user=User.objects.get(username=request.user),
                            discord_username=data['discord_username'],
                            discord_id=data['discord_id'],
                            email=data['email'],
                            subscription_date_expire=data['subscription_date_expire'],
                            notify_7=json.loads(request.POST.get('notify_7', 'false')),
                            notify_3=json.loads(request.POST.get('notify_3', 'false')),
                            notify_24h=json.loads(request.POST.get('notify_24h', 'false')),
                            is_invited=json.loads(request.POST.get('is_invited', 'false')),
                            is_activated=json.loads(request.POST.get('is_activated', 'false')),
                            )
            member.save()
            return HttpResponse(json.dumps({'status': 'OK'}), content_type='application/json')
        return HttpResponse(json.dumps({'status': 'NO', 'errors': [(v[0]) for k, v in form.errors.items()]}),
                            content_type='application/json')

    def delete(self, request):
        try:
            get_body = QueryDict(request.body)
            memberid = get_body['memberid']
            Member.objects.filter(user=User.objects.get(username=request.user), id=memberid).delete()
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'NO', 'errors': e.args}),
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'OK'}), content_type='application/json')


class MembersView(View):
    template_name = 'dashboard/members.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = MemberForm()
            return render(request=request, template_name=self.template_name, context={'menu': 'Members', 'form': form})
        return render(request, reverse_lazy('announceusio:login'), {'error': False})


class BotMessagesView(View):
    template_name = 'dashboard/bot_messages.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if BotMessage.objects.filter(user=User.objects.get(username=request.user)).exists():
                bot_message = BotMessage.objects.filter(user=User.objects.get(username=request.user)).values()[0]
                form = bot_message
            else:
                form = {}
            data = {'menu': 'Bot messages', 'form': form}
            return render(request, self.template_name, data)
        return render(request, reverse_lazy('announceusio:login'), {'error': False})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, reverse_lazy('announceusio:login'), {'error': False})
        body = dict()
        body['help_message_body'] = (request.POST['help_message_body']).strip()
        body['wrong_email'] = (request.POST['wrong_email']).strip()
        body['already_activated'] = (request.POST['already_activated']).strip()
        body['activated'] = (request.POST['activated']).strip()
        body['before_expiration'] = (request.POST['before_expiration']).strip()
        body['should_activate'] = (request.POST['should_activate']).strip()
        body['renewal_link'] = (request.POST['renewal_link']).strip()
        body['buy_membership'] = (request.POST['buy_membership']).strip()
        body['first_reminder'] = (request.POST['first_reminder']).strip()
        body['second_reminder'] = (request.POST['second_reminder']).strip()
        body['finely_reminder'] = (request.POST['finely_reminder']).strip()
        body['expired_reminder'] = (request.POST['expired_reminder']).strip()
        body['join_message'] = (request.POST['join_message']).strip()

        try:
            if BotMessage.objects.filter(user=User.objects.get(username=request.user)).exists():
                BotMessage.objects.filter(user=User.objects.get(username=request.user)).update(**body)
                return HttpResponse(json.dumps({'status': 'OK'}), content_type='application/json')
            return HttpResponse(json.dumps({'status': 'NO'}), content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'NO'}), content_type='application/json')


class UserSettingsView(View):
    template_name = 'dashboard/user_settings.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            try:
                user_profile = UserProfile.objects.get(user=user)
                form = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                    'company': user_profile.company
                }
                data = {'menu': 'User settings', 'form': form}
                return render(request, self.template_name, data)
            except Exception as e:
                pass
        return render(request, reverse_lazy('announceusio:login'), {'error': False})

    def post(self, request):
        if request.user.is_authenticated and request.POST:
            form = {}
            try:
                user = User.objects.get(username=request.user)
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['user_email']
                user.save()
                user_profile = UserProfile.objects.get(user=user)
                user_profile.company = request.POST['company']
                user_profile.save()
                form = {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                    'company': user_profile.company
                }
            except Exception as e:
                pass
            data = {'menu': 'User settings', 'form': form, 'status': 'OK'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        return render(request, self.template_name, {})


class BillingSettingsView(View):
    template_name = 'dashboard/billing.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(username=request.user)
                billing_settings = Billing.objects.filter(user=user).first()
                user_profile = UserProfile.objects.get(user=user)
                form = {
                    'price': billing_settings.price,
                    'item_name': billing_settings.item_name,
                    'paypal_email': billing_settings.paypal_email,
                    'sub_days': billing_settings.sub_days,
                }
                url = user_profile.company if user_profile.company else ''
                paypal_dict = {
                    "business": billing_settings.paypal_email,
                    "amount": billing_settings.price,
                    "item_name": billing_settings.item_name,
                    "invoice": "{}".format(str(uuid.uuid4())),
                    "notify_url": "https://cookstart.io" + reverse('paypal-ipn'),
                    "return": "https://" + url + str(reverse_lazy('announceusio:index')),
                    "cancel_return": "https://" + url + str(reverse_lazy('announceusio:index')),
                    "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
                }
                form_paypal = PayPalPaymentsForm(initial=paypal_dict)
                return render(request=request, template_name=self.template_name,
                              context={'menu': 'Billing', 'form': form, 'form_paypal': form_paypal})
            except Exception as e:
                return render(request=request, template_name=self.template_name,
                              context={'menu': 'Billing', 'form': {}, 'form_paypal': {}})
        return render(request, reverse_lazy('announceusio:login'), {'error': False})

    def post(self, request):
        if not request.user.is_authenticated and request.method != 'POST':
            return render(request, reverse_lazy('announceusio:login'), {'error': False})
        try:
            billing_settings = {
                'price': request.POST['price'],
                'item_name': request.POST['item_name'],
                'paypal_email': request.POST['paypal_email'],
                'sub_days': request.POST['sub_days'],
            }
            user = User.objects.get(username=request.user)
            if Billing.objects.filter(user_id=user.id).exists():
                Billing.objects.filter(user=user).update(**billing_settings)
            else:
                Billing.objects.update_or_create(user=user, **billing_settings)
            data = {'status': 'OK'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception as e:
            data = {'status': 'NO', 'error': e.args[1]}
            return HttpResponse(json.dumps(data), content_type='application/json')


class BotSettingsView(View):
    template_name = 'dashboard/bot_settings.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(username=request.user)
                bot_settings = BotSettings.objects.filter(user=user).first()
                form = {
                    'discord_channel_id': bot_settings.discord_channel_id,
                    'discord_server_id': bot_settings.discord_server_id,
                    'bot_token': bot_settings.bot_token,
                    'member_role': bot_settings.member_role
                }
                return render(request=request, template_name=self.template_name,
                              context={'menu': 'Bot settings', 'form': form})
            except Exception as e:
                return render(request=request, template_name=self.template_name,
                              context={'menu': 'Bot settings', 'form': {}})
        return render(request, reverse_lazy('announceusio:index'), {'error': False})

    def post(self, request):
        if not request.user.is_authenticated and request.method != 'POST':
            return render(request, reverse_lazy('announceusio:index'), {'error': False})
        try:
            bot_settings = {
                'discord_channel_id': request.POST['discord_channel_id'],
                'discord_server_id': request.POST['discord_server_id'],
                'bot_token': request.POST['bot_token'],
                'member_role': request.POST['member_role']
            }
            user = User.objects.get(username=request.user)
            if BotSettings.objects.filter(user=user).exists():
                BotSettings.objects.filter(user=user).update(**bot_settings)
            else:
                BotSettings.objects.update_or_create(user=user, **bot_settings)
            data = {'status': 'OK'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception as e:
            data = {'status': 'NO', 'error': e.args[1]}
            return HttpResponse(json.dumps(data), content_type='application/json')


class EmailSettingsView(View):
    template_name = 'dashboard/email_settings.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(username=request.user)
                email_settings = EmailSettings.objects.filter(user=user).first()
                form = {
                    'email': email_settings.email,
                    'email_password': email_settings.email_password,
                    'message_body': email_settings.message_body,
                    'email_subject': email_settings.email_subject
                }
                return render(request=request, template_name=self.template_name,
                              context={'menu': 'Email settings', 'form': form})
            except Exception as e:
                return render(request=request, template_name=self.template_name,
                              context={'menu': 'Email settings', 'form': {}})
        return render(request, reverse_lazy('announceusio:login'), {'error': False})

    def post(self, request):
        if not request.user.is_authenticated and request.method != 'POST':
            return render(request, reverse_lazy('announceusio:login'), {'error': False})
        try:
            email_settings = {
                'email': request.POST['email'],
                'email_password': request.POST['email_password'],
                'message_body': request.POST['message_body'],
                'email_subject': request.POST['email_subject'],
            }
            user = User.objects.get(username=request.user)
            if EmailSettings.objects.filter(user=user).exists():
                EmailSettings.objects.filter(user=user).update(**email_settings)
            else:
                EmailSettings.objects.update_or_create(user=user, **email_settings)
            data = {'status': 'OK'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception as e:
            data = {'status': 'NO', 'error': e.args[1]}
            return HttpResponse(json.dumps(data), content_type='application/json')


class OwnerView(View):
    template_name = 'dashboard/owner.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = UserCreationForm()
            return render(request, self.template_name, {'menu': 'Owner', 'form': form})
        return render(request, reverse_lazy('announceusio:login'), {'error': False})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, reverse_lazy('announceusio:login'), {'error': False})
        form = UserCreationForm(request.POST)
        print(request.POST['username'])
        if form.is_valid():
            try:
                form.save()
                super_admin = User.objects.get(username=request.user.username)
                owner = User.objects.get(username=request.POST['username'])
                user_profile = UserProfile.objects.create(user=owner)
                user_profile.save()
                bot_settings = BotSettings.objects.get(user=super_admin)
                bot_settings.pk = None
                bot_settings.user = owner
                bot_settings.save()
                email_settings = EmailSettings.objects.get(user=super_admin)
                email_settings.pk = None
                email_settings.user = owner
                email_settings.save()
                billing = Billing.objects.get(user=super_admin)
                billing.pk = None
                billing.user = owner
                billing.save()
                bot_message = BotMessage.objects.get(user=super_admin)
                bot_message.pk = None
                bot_message.user = owner
                bot_message.save()
                bot = BASE_DIR + "/paypal-discord-bot-admin.py"
                new_bot = BASE_DIR + f"/paypal-discord-bot-{request.POST['username']}.py"
                copyfile(bot, new_bot)
                f = open(new_bot, 'r')
                file_data = f.read()
                f.close()
                new_data = file_data.replace("OWNER_ID = 1", f"OWNER_ID = {owner.id}")
                f = open(new_bot, 'w')
                f.write(new_data)
                f.close()
                bot = BASE_DIR + "/paypal-discord-bot-admin.conf"
                new_bot = BASE_DIR + f"/paypal-discord-bot-{request.POST['username']}.conf"
                copyfile(bot, new_bot)
                f = open(new_bot, 'r')
                file_data = f.read()
                f.close()
                new_data = file_data.replace("paypal-discord-bot-admin", f"paypal-discord-bot-{owner.username}")
                f = open(new_bot, 'w')
                f.write(new_data)
                f.close()
                return render(request, self.template_name, {'form': form, 'success': 'Passed successfully!'})
            except Exception as e:
                form = UserCreationForm()
        return render(request, self.template_name, {'form': form, 'errors': [(v[0]) for k, v in form.errors.items()]})


class BotStatusView(View):

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated and request.method != 'POST':
            return render(request, reverse_lazy('announceusio:login'), {'error': False})
        try:
            url = f'http://{SERVER_SUPERVISOR_URL}/index.html'
            if request.POST['status'] == 'start':
                r = requests.get(f'{url}?processname=paypal-discord-bot-{request.user.username}&action=start',
                                 auth=(SERVER_SUPERVISOR_LOGIN, SERVER_SUPERVISOR_PASSWORD))
            elif request.POST['status'] == 'restart':
                r = requests.get(f'{url}?processname=paypal-discord-bot-{request.user.username}&action=restart',
                                 auth=(SERVER_SUPERVISOR_LOGIN, SERVER_SUPERVISOR_PASSWORD))
            elif request.POST['status'] == 'stop':
                r = requests.get(f'{url}?processname=paypal-discord-bot-{request.user.username}&action=stop',
                                 auth=(SERVER_SUPERVISOR_LOGIN, SERVER_SUPERVISOR_PASSWORD))

            data = {'status': 'OK'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        except Exception as e:
            data = {'status': 'NO', 'error': e.args[1]}
            return HttpResponse(json.dumps(data), content_type='application/json')


class PayPalIPNView(View):
    template_name = 'dashboard/paypal_ipn.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = PayPalForm()
            return render(request, self.template_name, {'menu': 'PayPal IPN', 'form': form})
        return render(request, reverse_lazy('announceusio:login'), {'error': False})


class PayPalTableView(View):

    def get(self, request, *args, **kwargs):
        try:
            ajax_response = {'sEcho': '', 'aaData': [], 'iTotalRecords': 0, 'iTotalDisplayRecords': 0}
            owner_members_email_list = Member.objects.filter(user=User.objects.get(username=request.user)).values_list('email', flat=True)
            user = User.objects.get(username=request.user)
            billing = Billing.objects.get(user=user)
            paypal_ipns = PayPalIPN.objects.filter(business=billing.paypal_email)
            if not paypal_ipns:
                return HttpResponse(json.dumps(ajax_response), content_type='application/json')
            list_name = ['invoice', 'receiver_id', 'flag', 'flag_info', 'custom', 'payment_status',
                         'created_at']
            # search
            search = request.GET.get('search[value]', '')
            if search:
                pass
                paypal_ipns = paypal_ipns.filter(
                    Q(invoice__icontains=search) | Q(flag_info__icontains=search)
                    | Q(custom__icontains=search) | Q(payment_status__icontains=search))
            # Sorting
            sort_column = list_name[int(request.GET.get('order[1][column]', 0))]
            if request.GET.get('order[0][dir]', None) == 'desc':
                sort_column = '-{}'.format(sort_column)
            paypal_ipns = paypal_ipns.order_by(sort_column)
            # filter
            # discord_username = request.GET.get('columns[1][search][value]', False)
            # discord_id = request.GET.get('columns[3][search][value]', False)
            # email = request.GET.get('columns[2][search][value]', False)
            #
            # if discord_username or discord_id or email:
            #     members = paypal_ipns.filter(
            #         (Q(invoice=invoice) if invoice else Q())
            #         & (Q(description=discord_id) if discord_id else Q())
            #         & (Q(category=email) if email else Q())
            #     )
            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            ajax_response['iTotalRecords'] = ajax_response['iTotalDisplayRecords'] = paypal_ipns.count()
            for paypal_ipn in paypal_ipns[start:start + length]:
                ajax_response['aaData'].append(
                    [
                        paypal_ipn.id,
                        str(paypal_ipn.__unicode__()).replace('<', '< '),
                        paypal_ipn.flag,
                        paypal_ipn.flag_info,
                        paypal_ipn.invoice,
                        paypal_ipn.custom,
                        paypal_ipn.payment_status,
                        str((paypal_ipn.created_at).strftime('%B %d, %Y, %I:%M')
                            + paypal_ipn.created_at.strftime(' %p').lower()),
                        paypal_ipn.id,
                        paypal_ipn.id
                    ])
            return HttpResponse(json.dumps(ajax_response), content_type='application/json')
        except Exception as e:
            pass

    def delete(self, request):
        try:
            get_body = QueryDict(request.body)
            if get_body.get('id', False):
                paypal_id = get_body.get('id')
                paypal_model = PayPalIPN.objects.get(id=paypal_id)
            elif get_body.getlist('id[]', False):
                paypal_ids_list = [int(i) for i in get_body.getlist('id[]')]
                paypal_model = PayPalIPN.objects.filter(id__in=paypal_ids_list)
            else:
                return HttpResponse(json.dumps({'status': 'NO'}), content_type='application/json')
            paypal_model.delete()
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'NO', 'errors': e.args}),
                                content_type='application/json')
        return HttpResponse(json.dumps({'status': 'OK'}), content_type='application/json')
