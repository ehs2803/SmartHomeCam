from base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
 	'default': {
     'ENGINE': 'django.db.backends.mysql',
     'NAME':  "smarthomecam",
     'USER': "root",
     'PASSWORD': "1234",
     'HOST': 'localhost',
     'PORT': '3306',
     }
}