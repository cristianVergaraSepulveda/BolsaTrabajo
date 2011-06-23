# Django settings for BolsaTrabajo project.

import os, sys

PROJECT_ROOT = '/'.join(os.path.dirname(__file__).split('/')[0:-1])

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Gabriel Gayan', 'gabrielgayan@gmail.com'),
    ('Vijay Khemlani', 'vkhemlan@gmail.com'),
)

# Set email configuration at local.py

# EMAIL_HOST = 'host'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'user'
# EMAIL_HOST_PASSWORD = 'password'
# EMAIL_USE_TLS = True
# EMAIL_FULL_ADDRESS = 'address'

SERVER_NAME = 'http://127.0.0.1:8000'

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = 'bolsa_trabajo.models.UserProfile'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'bolsa_trabajo.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/Santiago'

LANGUAGE_CODE = 'es-cl'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/admin_media/'

SECRET_KEY = "lala"

LOGIN_URL = '/account/login/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'djangoflash.context_processors.flash',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangoflash.middleware.FlashMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',

    #third party
    'south',

    #our apps
    'bolsa_trabajo',
)

# Avoid migrating database when running tests
SOUTH_TESTS_MIGRATE = True

# Application settings
OFFER_EXPIRATION_LIMIT = 30 # in days
