from rest_framework import permissions


class IsParticipantOrSender(permissions.BasePermission):
    """
    Custom permission to allow only conversation participants to send, view,
    update, and delete messages.
    """

    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For Message objects
        if hasattr(obj, "conversation"):
            is_participant = user in obj.conversation.participants.all()

            if request.method in ["PUT", "PATCH", "DELETE"]:
                # Only allow participants to update or delete messages
                return is_participant and obj.sender == user

            return is_participant

        # For Conversation objects
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        return False
