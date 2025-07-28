from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingSignalTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello!")
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
        self.assertEqual(notification.message, msg)
