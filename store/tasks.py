from celery import shared_task
from django.contrib.auth.models import User
from templated_mail.mail import BaseEmailMessage
from django.core.mail import BadHeaderError

@shared_task
def notify_customer(user_id):
    try:
        user = User.objects.get(id=user_id)
        message = BaseEmailMessage(
            template_name='email/order_email_template.html', context={'name': user.first_name})
        message.send(to=[user.email])
    except BadHeaderError:
        pass