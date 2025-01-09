from celery import shared_task
from templated_mail.mail import BaseEmailMessage
from django.core.mail import BadHeaderError

@shared_task
def notify_customer(message):
    try:
        message = BaseEmailMessage(
            template_name='email/order_email_template.html', context={'name': 'Linxuan'})
        message.send(to=['purelala233@gmail.com'])
    except BadHeaderError:
        pass