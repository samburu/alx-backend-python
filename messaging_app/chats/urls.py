from django.urls import include, path
from rest_framework_nested.routers import NestedDefaultRouter

from .views import ConversationViewSet, MessageViewSet

# Main router
router = NestedDefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

# Nested router for messages within conversations
messages_router = NestedDefaultRouter(
    router, r"conversations", lookup="conversation"
)
messages_router.register(
    r"messages", MessageViewSet, basename="conversation-messages"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(messages_router.urls)),
]
