from celery import shared_task
from time import sleep
from templated_mail.mail import BaseEmailMessage
from django.core.mail import BadHeaderError

@shared_task
def notify_customer(message):
    try:
        message = BaseEmailMessage(
            template_name='email/order_email_template.html', context={'name': 'Linxuan'})
        message.from_email = 'Linxu2'
        message.send(to=['xx@231.com'])
    except BadHeaderError:
        pass