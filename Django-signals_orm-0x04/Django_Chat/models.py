from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_threaded_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_threaded_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:30]}"
    
    
    def get_thread(self):
    """ Recursively fetch all replies in threaded format """
    thread = []

    def recurse(message):
        replies = message.replies.all().order_by('timestamp')
        for reply in replies:
            thread.append(reply)
            recurse(reply)

    recurse(self)
    return thread

