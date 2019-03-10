"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+dfp4%c@v^k-sixv@2h=%q1t35r1$6!b8q!@=he+c9)x)ue-!@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["announceus.io", "127.0.0.1", "45.79.0.173", 'cookstart.io', 'dashboard.cookstart.io']


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangobower',
    'crispy_forms',
    'paypal.standard.ipn',
    'announceusio',
    'website'
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'announceusio.middleware.GetCompany'
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 3000, 
        # 'NAME': 'db_django',
        'NAME': 'db_discord',
        'USER': 'root',
        # 'PASSWORD': 'aw@ewq2zAd',
        'PASSWORD': '789456',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS':{
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': 'SET foreign_key_checks = 0;',
            },
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder'
)

#STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_ROOT = '/home/discord/discord/website/admin/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

BOWER_INSTALLED_APPS = [
    'components-font-awesome#4.7.0',
    'datatables.net#1.10.19',
    'datatables.net-autofill#2.3.2',
    'datatables.net-autofill-dt#2.3.2',
    'datatables.net-buttons#1.5.4',
    'datatables.net-buttons-dt#1.5.4',
    'datatables.net-colreorder#1.5.1',
    'datatables.net-colreorder-dt#1.5.1',
    'datatables.net-dt#3.2.2',
    'datatables.net-fixedcolumns#3.2.6',
    'datatables.net-fixedcolumns-dt#3.2.6',
    'datatables.net-fixedheader#3.1.5',
    'datatables.net-fixedheader-dt#3.1.5',
    'datatables.net-keytable#2.5.0',
    'datatables.net-keytable-dt#2.5.0',
    'datatables.net-responsive#2.2.3',
    'datatables.net-responsive-dt#2.2.3',
    'datatables.net-rowgroup#1.1.0',
    'datatables.net-rowgroup-dt#1.1.0',
    'datatables.net-rowreorder#1.2.5',
    'datatables.net-rowreorder-dt#1.2.5',
    'datatables.net-scroller#1.5.1',
    'datatables.net-scroller-dt#1.5.1',
    'datatables.net-select#1.2.7',
    'datatables.net-select-dt#1.2.7',
    'jquery#3.3.1',
    'underscore#1.9.1'
]

# Paypal

#PAYPAL_RECEIVER_EMAIL = "lastrit@hotmail.com"
PAYPAL_TEST = True
