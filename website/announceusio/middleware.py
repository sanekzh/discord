from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User

from .models import UserProfile


class GetCompany(MiddlewareMixin):
    def process_request(self, request):
        try:

            user_profile = UserProfile.objects.filter(user=User.objects.get(username=request.user)).first()
            url = user_profile.company if user_profile.company else ''
            request.url = url
            return None
        except Exception as e:
            return None


class GetUsername(MiddlewareMixin):
    def process_request(self, request):
        try:
            user_profile = UserProfile.objects.filter(user=User.objects.get(username=request.user)).first()
            request.user_name = user_profile.company.capitalize() if user_profile.company else ''
            return None
        except Exception as e:
            return None