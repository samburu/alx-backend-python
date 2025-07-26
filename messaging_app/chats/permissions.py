from rest_framework import permissions

class IsParticipantOrSender(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own conversations or messages.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if hasattr(obj, "participants"):  # It's a Conversation
            return user in obj.participants.all()
        elif hasattr(obj, "sender") and hasattr(obj, "conversation"):  # It's a Message
            return obj.sender == user or user in obj.conversation.participants.all()

        return False
