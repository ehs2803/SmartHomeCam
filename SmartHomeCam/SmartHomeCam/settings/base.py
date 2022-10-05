"""
Django settings for SmartHomeCam project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
import json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# secret_file = os.path.join(BASE_DIR, 'secrets.json')
#
# with open(secret_file) as f:
#     secrets = json.loads(f.read())


# Keep secret keys in secrets.json
# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         error_msg = "Set the {0} environment variable".format(setting)
#         raise ImproperlyConfigured(error_msg)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vtmc*^z@#g=6#l@+pblp74iw@$k!)-48cnk)6!ft*7*bl!#6sm'
#SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-vtmc*^z@#g=6#l@+pblp74iw@$k!)-48cnk)6!ft*7*bl!#6sm')


# if os.environ.get('DJANGO_ALLOWED_HOSTS'):
#     ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')
# else:

AWS_ACCESS_KEY_ID_SNS = os.environ.get('AWS_ACCESS_KEY_ID_SNS','temp')
AWS_SECRET_ACCESS_KEY_SNS = os.environ.get('AWS_SECRET_ACCESS_KEY_SNS','temp')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD','temp')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'account',
    'mainpage',
    'mypage',
    'homecam',
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

ROOT_URLCONF = 'SmartHomeCam.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'SmartHomeCam.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# s3
AWS_ACCESS_KEY_S3 = os.environ.get('AWS_ACCESS_KEY_S3')
AWS_SECRET_KEY_S3 = os.environ.get('AWS_SECRET_KEY_S3')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
S3_BUCKET_REGION = os.environ.get('S3_BUCKET_REGION')
S3_BUCKET_DIR = os.environ.get('S3_BUCKET_DIR')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '_static')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 미디어 파일을 관리할 루트 media 디렉터리
MEDIA_ROOT = os.path.join(BASE_DIR, '_media')
# 각 media file에 대한 URL prefix
MEDIA_URL = '/media/'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# login url
LOGIN_REDIRECT_URL = ''
