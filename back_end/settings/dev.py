from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-mtfnjr^5hhd_lvcgtk3(m&&=!tbhqm1=j!rwmbi8wx_)0xu$&u'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'store_demo_database',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '940620Chen!'
    }
}

if DEBUG:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        'silk.middleware.SilkyMiddleware',
        *MIDDLEWARE,
    ]