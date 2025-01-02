from .common import *
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS: List = []

# Database settings

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

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "storages",
]
