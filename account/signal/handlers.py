from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from store.models import Customer


@receiver(signal=post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_on_user_create(sender, **kwargs):
    user = kwargs['instance']

    if kwargs['created']:
        Customer.objects.create(
            user=user, first_name=user.first_name, last_name=user.last_name)
