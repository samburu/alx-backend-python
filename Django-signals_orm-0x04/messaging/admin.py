from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for the Message model.
    """

    list_display = ("sender", "recipient", "subject", "timestamp", "is_read")
    search_fields = ("sender__username", "recipient__username", "subject")
    list_filter = ("is_read", "timestamp")
    ordering = ("-timestamp",)
