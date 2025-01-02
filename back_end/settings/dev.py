from .common import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

SECRET_KEY = 'django-insecure-mtfnjr^5hhd_lvcgtk3(m&&=!tbhqm1=j!rwmbi8wx_)0xu$&u'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'demo_store',
        'USER': os.environ.get('RDS_DATABASE_USER'),
        'PASSWORD': os.environ.get('RDS_DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '3307',
    }
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

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
