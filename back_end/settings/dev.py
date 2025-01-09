from .common import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo_store',
        'USER': os.environ.get('RDS_DATABASE_USER'),
        'PASSWORD': os.environ.get('RDS_DATABASE_PASSWORD'),
        'HOST': 'host.docker.internal',
        'PORT': '3307',
    }
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

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

EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

# supervisor settings
INSTALLED_APPS = [
    *INSTALLED_APPS,
    "storages",
    "debug_toolbar",
]
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'silk.middleware.SilkyMiddleware',
    *MIDDLEWARE,
]
