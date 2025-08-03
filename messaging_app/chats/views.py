from rest_framework import filters, permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.shortcuts import render

from .models import Conversation, Message
from .permissions import IsParticipantOrSender
from .serializers import ConversationSerializer, MessageSerializer
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Conversations.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOrSender, IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at"]


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Messages in Conversations.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOrSender, IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["sent_at"]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation_id")

        if not conversation_id:
            return Message.objects.none()

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Message.objects.none()

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                "You are not a participant of this conversation.",
                code=status.HTTP_403_FORBIDDEN
            )

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation")
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(
                "You are not a participant of this conversation.",
                code=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user)


@cache_page(60)
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).order_by("timestamp")
    return render(request, "chats/conversation.html", {"messages": messages})