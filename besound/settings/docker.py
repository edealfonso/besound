"""Settings for running besound inside Docker (see docker-compose.yml).

Everything is configured through environment variables.
"""
import os

from .base import *

DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = config_list('DJANGO_CSRF_TRUSTED_ORIGINS', ['http://localhost:8000'])

# Always https, except when debugging locally on http://localhost (DJANGO_DEBUG=1)
if not DEBUG:
    globals().update(https_settings())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'besound'),
        'USER': os.environ.get('POSTGRES_USER', 'besound'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Static and media files are served by nginx (see docker/nginx.conf)
STATIC_URL = '/static/'
