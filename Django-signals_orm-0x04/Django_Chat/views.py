from django.shortcuts import render
# views.py or Django shell
from .models import Message
from django.contrib.auth.models import User

def get_user_conversations(user):
    # Get all messages where the user is sender or receiver and fetch parent and replies efficiently
    return (
        Message.objects.filter(sender=user)
        .select_related('parent_message', 'sender', 'receiver')
        .prefetch_related('replies')
    )
