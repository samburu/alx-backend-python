from django.test import TestCase
from django.contrib.auth.models import User

from .models import Message


class MessageModelTest(TestCase):
    """
    Test case for the Message model.
    """

    def setUp(self):
        """
        Create test users and a message.
        """
        self.user1 = User.objects.create_user(
            username="alice", password="password"
        )
        self.user2 = User.objects.create_user(
            username="bob", password="password"
        )

    def test_message_creation(self):
        """
        Test that the message is created correctly.
        """
        message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            subject="Test Subject",
            body="This is a test message.",
        )
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.recipient, self.user2)
        self.assertEqual(message.subject, "Test Subject")
        self.assertEqual(message.body, "This is a test message.")
        self.assertFalse(message.is_read)
