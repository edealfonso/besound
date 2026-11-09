"""Settings configured through environment variables.

Used by the Docker image, both locally (docker-compose.yml) and in production
(Render + Neon + Cloudflare R2, see docs/DESPLIEGUE.md).
"""
import os

import dj_database_url

from .base import *

DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

ALLOWED_HOSTS = config_list('DJANGO_ALLOWED_HOSTS', ['localhost', '127.0.0.1'])

CSRF_TRUSTED_ORIGINS = config_list('DJANGO_CSRF_TRUSTED_ORIGINS', ['http://localhost:8000'])

# On Render, its public hostname (xxx.onrender.com) is added automatically
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])
    CSRF_TRUSTED_ORIGINS.append('https://' + os.environ['RENDER_EXTERNAL_HOSTNAME'])

# Always https, except when debugging locally on http://localhost (DJANGO_DEBUG=1)
if not DEBUG:
    globals().update(https_settings())

# Database: DATABASE_URL (e.g. Neon) or the POSTGRES_* variables (docker-compose)
if os.environ.get('DATABASE_URL'):
    DATABASES = {'default': dj_database_url.config(conn_max_age=60, conn_health_checks=True)}
else:
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

# Static files: served by Django itself with whitenoise (no nginx needed on Render)
STATIC_URL = '/static/'
MIDDLEWARE.insert(MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
                  'whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# Media files (audio): Cloudflare R2 when configured, otherwise the local disk
if os.environ.get('R2_BUCKET_NAME'):
    STORAGES['default'] = {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'bucket_name': os.environ['R2_BUCKET_NAME'],
            'endpoint_url': os.environ['R2_ENDPOINT_URL'],  # https://<account id>.r2.cloudflarestorage.com
            'access_key': os.environ['R2_ACCESS_KEY_ID'],
            'secret_key': os.environ['R2_SECRET_ACCESS_KEY'],
            'region_name': 'auto',
            'signature_version': 's3v4',
            # Public URL of the bucket (r2.dev subdomain or a custom domain). Accepted with
            # or without https:// and trailing slash: storages adds the scheme itself
            'custom_domain': os.environ['R2_PUBLIC_DOMAIN'].split('://')[-1].rstrip('/'),
            'querystring_auth': False,
            'file_overwrite': False,
            'default_acl': None,
        },
    }
