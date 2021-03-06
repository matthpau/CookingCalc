"""
Django settings for CookingBase project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from . import my_secrets

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#My Production Base Dir, used in a few places for checking if we are on the pdn server
BASE_DIR_PDN = os.path.expanduser('~/matthpau.pythonanywhere.com/CookingCalc/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = my_secrets.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

# for sending emails to the console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Email Setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = 'your.local.stores.ch@gmail.com'
EMAIL_HOST_PASSWORD = my_secrets.EMAIL_HOST_PASSWORD

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS = [

    #https://django-modeltranslation.readthedocs.io/en/latest/index.html #Needs to go before admin
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    'django.contrib.humanize',

    # Local
    'users.apps.UsersConfig',
    'AppTimesCalc.apps.ApptimesCalcConfig',
    'RecipeConverter.apps.RecipeconverterConfig',
    'stores.apps.StoresConfig',
    'newsletters.apps.NewslettersConfig',

    #https://django-allauth.readthedocs.io/en/latest/installation.html
    #important - this MUST come after the local apps are registered
    # 3rd party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    #Datepicker https://github.com/monim67/django-bootstrap-datepicker-plus
    'bootstrap_datepicker_plus',

    #https://django-crispy-forms.readthedocs.io/en/latest/index.html
    'crispy_forms',

    #https://django-taggit.readthedocs.io/en/stable/index.html
    'taggit',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CookingBase.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request', #Allauth
            ],
        },
    },
]

WSGI_APPLICATION = 'CookingBase.wsgi.application'

# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

#forproduction
#For Local PostGres SQL
#https://postgresapp.com/

if os.path.exists(BASE_DIR_PDN):            #We are on the production server
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "cookingcalc",
            "USER": "super",
            "PASSWORD": my_secrets.POSTGRES_PDN_PWD,
            "HOST": "matthpau-1212.postgres.pythonanywhere-services.com",
            "PORT": "11212",
        }
    }
    DEBUG = False
else:           
    print('Using the local dev DB, debug is TRUE', os.getpid())   # we are on the dev machine
    #Why runs twice? https://stackoverflow.com/questions/16546652/why-does-django-run-everything-twice
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "paulmatthews",
            "USER": "paulmatthews",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "",
        }
    }
    DEBUG = True

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
#Note - need to run SET GLOBAL time_zone = '+01:00'; in mySQL to make them compatible

#required for https://django-modeltranslation.readthedocs.io/en/latest/installation.html#setup
gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('de', gettext('German')),
)


USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

#for Python Anywhere collection
STATIC_ROOT = "/home/matthpau/matthpau.pythonanywhere.com/CookingCalc/pa_static"

AUTH_USER_MODEL = 'users.CustomUser'

SITE_ID = 1


# AllAuth reuirements
# https://django-allauth.readthedocs.io/en/latest/index.html

LOGIN_REDIRECT_URL = 'Home' #could also be 'Home'
LOGOUT_REDIRECT_URL = 'Home' #Original Django
ACCOUNT_LOGOUT_REDIRECT_URL = '/' #Allauth

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = None


#used because I want to serialize time data and JSON doesn't like this
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#my settings for usage during various operaetions
ARCHIVE_USERNAME = 'archive_user'
ARCHIVE_USER_EMAIL = 'archive_user@cooking-helpers.com'

#GeoIP settings
GEOIP_PATH = os.path.join(BASE_DIR, 'geo_data')

#Required for translation
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
