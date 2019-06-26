"""
Django settings for CookingBase project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'id6@3=!641uy35qbz#@r#b^5nr4y_igzj4*m__=a6kl4fmf=w7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

# for sending emails to the console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Email Setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = 'cooking.helpers.reset@gmail.com'
EMAIL_HOST_PASSWORD = 'tupaki123'


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Local
    'users.apps.UsersConfig',
    'AppTimesCalc.apps.ApptimesCalcConfig',
    'RecipeConverter.apps.RecipeconverterConfig',

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

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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

 Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

#forproduction
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'matthpau$CookingCalc',
         'USER': 'matthpau',
         'PASSWORD': 'matthpaucookingpw',
         'HOST': 'matthpau.mysql.pythonanywhere-services.com',
         'PORT': '3306',
     }
 }

"""
for local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""


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


#used because I want to serialize time data and JSON doesn't like this
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#my settings for usage during various operaetions
ARCHIVE_USERNAME = 'archive_user'
ARCHIVE_USER_EMAIL = 'archive_user@cooking-helpers.com'
