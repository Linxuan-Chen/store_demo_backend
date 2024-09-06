import os
from celery import Celery
# set env variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')

celery = Celery('back_end')
# load config from django.conf.settings, and set config prefix as CELERY
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()