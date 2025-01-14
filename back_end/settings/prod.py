from .common import *
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = False

ALLOWED_HOSTS: List = ['35.183.186.59', 'localhost']

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'http://35.183.186.59']

# Database settings

# For dev purpose only
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'demo_store',
#         'USER': os.environ.get('RDS_DATABASE_USER'),
#         'PASSWORD': os.environ.get('RDS_DATABASE_PASSWORD'),
#         'HOST': 'host.docker.internal',
#         'PORT': '3307',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('RDS_DATABASE_NAME'),
        'HOST': os.environ.get('RDS_DATABASE_HOST'),
        'PORT': os.environ.get('RDS_DATABASE_PORT', '3306'),
        'USER': os.environ.get('RDS_DATABASE_USER'),
        'PASSWORD': os.environ.get('RDS_DATABASE_PASSWORD')
    }
}

# AWS Settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": os.environ.get('AWS_STORAGE_BUCKET_NAME'),
            "custom_domain": os.environ.get('AWS_S3_CUSTOM_DOMAIN'),
            "file_overwrite": False,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Media URL for S3
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# SMTP settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 465  
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', "")
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', "")
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', "") 

CELERY_BROKER_URL = 'redis://redis:6379/1'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/2',
        'TIMEOUT': 10 * 60,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "storages",
]
