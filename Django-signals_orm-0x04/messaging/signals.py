from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message


@receiver(post_save, sender=Message)
def notify_user_on_message(sender, instance, created, **kwargs):
    """
    Signal to notify user when a new message is created.
    """
    if created:
        # Here you would typically send a notification to the user
        # For example, using Django's built-in messaging framework or an external service
        print(
            f"Notification: New message from {instance.sender} to {instance.recipient}"
        )
        # You can also implement logic to send emails or push notifications here
