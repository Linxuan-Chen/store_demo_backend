from .common import *
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = False

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

# SMTP settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_USE_TLS = True 
EMAIL_HOST_USER = 'linxuanchen2017@gmail.com'  # Gmail 地址
EMAIL_HOST_PASSWORD = 'your-gmail-password'  # Gmail 密码 (如果启用两步验证，使用应用专用密码)
DEFAULT_FROM_EMAIL = 'your-gmail-address@gmail.com'  # 默认发件人邮箱

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "storages",
]
