import os
from django.utils.translation import ugettext_lazy as _


DEBUG = (os.environ.get('DJANGO_ENV', '') != 'prod')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    'django_ajax',
    'el_pagination',
    'storages',
    'blog',
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
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

# File Storage Backend
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

AWS_S3_REGION_NAME = 'ap-northeast-2'

AWS_IS_GZIPPED = True


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USERNAME'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ.get('DB_PORT', 5432),
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
LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

# Endless pagination
EL_PAGINATION_PER_PAGE = 5

MARKUP_SETTINGS = {
    'markdown': {
        'safe_mode': False
    }
}
