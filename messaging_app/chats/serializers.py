from rest_framework import serializers

from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]

    def validate_role(self, value):
        allowed_roles = ["guest", "host", "admin"]
        if value not in allowed_roles:
            raise serializers.ValidationError(
                f"Invalid role '{value}'. Allowed roles are: {', '.join(allowed_roles)}."
            )
        return value


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at", "messages"]

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data
