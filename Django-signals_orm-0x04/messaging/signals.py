from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message, Notification


@receiver(post_save, sender=Message)
def notify_user_on_message(sender, instance, created, **kwargs):
    """
    Signal to notify user when a new message is created.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
