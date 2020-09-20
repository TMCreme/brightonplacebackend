"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'brightonplace18@gmail.com'
EMAIL_HOST_PASSWORD = 'kharis16'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%kn*hytw!ta295w_5a*kwr)$vlk0)26y9nmw9%)-06tnr@1d&)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['brightonplace.herokuapp.com']

LOGIN_REDIRECT_URL = '/home/edit_profile/'
LOGIN_URL = '/home/'
LOGOUT_REDIRECT_URL = '/home'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_jwt',
    'rest_auth',
    'django_rest_passwordreset',
    'widget_tweaks',
    'crispy_forms',
    'multiselectfield',
    'home',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

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
                'home.context_processors.baseview',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'da81jasqgs8emg',
        'USER': 'pcoljrxrqxdxnu',
        'PASSWORD': 'fada0d25e38be339657e6f917772b6e4daee4527a69dfa0bd8d37dc956c1153b',
        'HOST': 'ec2-54-225-92-1.compute-1.amazonaws.com',
        'PORT': '5432',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


from firebase_admin import messaging, firestore, initialize_app

config = {
      "apiKey": "AIzaSyDjSJmRlPe8m09XdRUqzFrEKEKKdwNu3hE",
      "authDomain": "chatprojectonny.firebaseapp.com",
      "databaseURL": "https://chatprojectonny.firebaseio.com",
      "projectId": "chatprojectonny",
      "storageBucket": "chatprojectonny.appspot.com",
      "messagingSenderId": "348714289467"
    }

initialize_app(config)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    )
}
import datetime

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=31536000),
}


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)


"""
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

#MEDIA_URL = 'https://s3.us-east-2.amazonaws.com/dziedzormdelasi/'

#MEDIA_ROOT = "https://s3.us-east-2.amazonaws.com/dziedzormdelasi/")
~~~~~~~~~~

#Amazon AWS s3 configuration
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AWS_ACCESS_KEY_ID = 'AKIAJIUBN2QO3N6J3QIQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'brightonplace'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

AWS_MEDIA_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)
MEDIA_ROOT = MEDIA_URL

DEFAULT_FILE_STORAGE = 'myproject.storage_backends.MediaStorage'
"""

#Microsoft azure configuration
DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = "brightonplace"

AZURE_ACCOUNT_KEY = '5khXI61UI8z92feb7r8LZoksn8BROeS2RdFujW9WQCP+qBqCHTW9shInhJuyaItNlc9Lm2RKNiphsUwrIH1Daw=='

AZURE_CONTAINER = 'static'

STATIC_URL = "https:brightonplace.blob.core.windows.net/static/"
MEDIA_ROOT = "https:brightonplace.blob.core.windows.net"

MEDIA_URL = "https:brightonplace.blob.core.windows.net/media/"
















