# -*- coding: utf-8 -*-

import os
import settings_var
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_var.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'localhost.',
    '.lynlab.co.kr',
    '.lynlab.co.kr.',
    '128.199.104.189',
    '128.199.104.189.'
]


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django_multimarkup',
    'django_ajax',
    'templatetags',
    'el_pagination',
    'simple_wiki',
    'blog',
    'dashboard',
    'media',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'simple_wiki.context_processors.wiki',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGES = [
    ('ko', _('Korean')),
    ('en', _('English')),
    ('ja', _('Japanese')),
]

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = ( os.path.join('static'), )

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'lynlab.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'INFO',
        },
        'wiki': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
}

# Email backends

ACCOUNT_ACTIVATION_DAYS = 2

DEFAULT_FROM_EMAIL = 'admin@lynlab.co.kr'

EMAIL_HOST = 'localhost'

EMAIL_PORT = 25

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Wiki

WIKI_NAME = "LYnWiki α"

WIKI_SLOGAN = "전 지구상의 잡지식 집합소"


# Social OAuth backends

TWITTER_ACCOUNT = settings_var.TWITTER_ACCOUNT

TWITTER_KEY = settings_var.TWITTER_KEY

TWITTER_SECRET = settings_var.TWITTER_SECRET

TWITTER_ACCESS_KEY = settings_var.TWITTER_ACCESS_KEY

TWITTER_ACCESS_SECRET = settings_var.TWITTER_ACCESS_SECRET

LOGIN_URL = '/oauth/twitter/login'

LOGOUT_URL = '/oauth/twitter/logout'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'


# Endless pagination

EL_PAGINATION_PER_PAGE = 5
