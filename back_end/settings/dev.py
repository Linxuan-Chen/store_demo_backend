from .common import *
from dotenv import load_dotenv

load_dotenv()

DEBUG = True

# Database

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend', '35.183.186.59']

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'http://35.183.186.59']

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

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL = ''

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

# supervisor settings
INSTALLED_APPS = [
    *INSTALLED_APPS,
    "silk",
    "storages",
    "debug_toolbar",
]
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'silk.middleware.SilkyMiddleware',
    *MIDDLEWARE,
]
