from rest_framework.test import APITestCase
from django.urls import reverse
from .models import User, Conversation

class ChatTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test1", email="test1@test.com", password="123")
        self.user2 = User.objects.create_user(username="test2", email="test2@test.com", password="123")

        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])

    def test_create_conversation(self):
        url = reverse('conversation-list')
        res = self.client.post(url, {
            'participants': [str(self.user1.user_id), str(self.user2.user_id)]
        }, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('conversation_id', res.data)

    def test_send_message(self):
        url = reverse('conversation-messages-list', args=[self.conversation.conversation_id])
        res = self.client.post(url, {
            'sender': str(self.user1.user_id),
            'conversation': str(self.conversation.conversation_id),
            'message_body': 'Hello there!'
        }, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['message_body'], 'Hello there!')
