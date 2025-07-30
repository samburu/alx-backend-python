from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Message, Notification


@receiver(post_save, sender=Message)
def notify_user_on_message(sender, instance, created, **kwargs):
    """
    Signal to notify user when a new message is created.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to track message history before saving.
    This can be used to update read status or other attributes.
    """
    if instance.pk:
        # If the message already exists, we can update its history
        try:
            previous_message = Message.objects.get(pk=instance.pk)
            # If the read status has changed, we can log this change
            MessageHistory.objects.create(
                user=instance.receiver,
                message=instance,
                is_read=instance.is_read,
            )
            instance.is_edited = True  # Mark as edited if it exists
        except Message.DoesNotExist:
            pass
