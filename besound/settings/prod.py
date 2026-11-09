import mimetypes

from .base import *

mimetypes.add_type("text/css", ".css", True)


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG', '0') in ('1', 'True', 'true', True)

# CSRF_TRUSTED_ORIGINS = ['https://contemporaryartnow.com', 'https://www.contemporaryartnow.com']
# ALLOWED_HOSTS = ['contemporaryartnow.com', 'www.contemporaryartnow.com']
# Set ALLOWED_HOSTS in secret.json (list) or as env var (comma separated) to your API domain
ALLOWED_HOSTS = config_list('ALLOWED_HOSTS', ['*'])

# Production is always served over https
globals().update(https_settings())


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DB_NAME_PROD'),
        'USER': get_secret('USER_PROD'),
        'PASSWORD': get_secret('PASSWORD_PROD'),
        'HOST': 'localhost',
        'PORT': get_secret('DB_PORT'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/staticfiles/'

