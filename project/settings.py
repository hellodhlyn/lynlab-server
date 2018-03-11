import os
from django.utils.translation import ugettext_lazy as _

import pymysql

pymysql.install_as_MySQLdb()

DEBUG = (os.environ.get('DJANGO_ENV', '') != 'prod')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = [
    'localhost',
    'localhost.',
    '.lynlab.co.kr',
    '.lynlab.co.kr.',
]

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django_markup',
    'django_ajax',
    'templatetags',
    'el_pagination',
    'blog',
    'dashboard',
    'media',
    'moneybook',
    'wiki',
    'storage',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'lynlab/templates/')],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USERNAME'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '3306',
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
STATIC_ROOT = '/var/lynlab/static/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join('static'),)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
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
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
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

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_USER = 'HelloDHLyn'

EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

EMAIL_PORT = 587

EMAIL_USE_TLS = True

# Social OAuth backends
TWITTER_ACCOUNT = os.environ.get('TWITTER_ACCOUNT')

TWITTER_KEY = os.environ.get('TWITTER_KEY')

TWITTER_SECRET = os.environ.get('TWITTER_SECRET')

TWITTER_ACCESS_KEY = os.environ.get('TWITTER_ACCESS_KEY')

TWITTER_ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

# Endless pagination
EL_PAGINATION_PER_PAGE = 5

MARKUP_SETTINGS = {
    'markdown': {
        'safe_mode': False
    }
}

# Stoarge
MEDIA_ROOT = os.path.join(BASE_DIR, 'storage/objects')
