from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to users who are participants in the conversation.
    Assumes the view has a `get_object()` or `get_queryset()` method that returns a message or conversation.
    """

    def has_permission(self, request, view):
        # Only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Checks if the authenticated user is a participant of the related conversation.
        Handles both Conversation and Message objects.
        """
        conversation = None

        # Check if obj is a Conversation or related to one
        if hasattr(obj, 'participants'):
            conversation = obj
        elif hasattr(obj, 'conversation'):
            conversation = obj.conversation

        if conversation:
            return request.user in conversation.participants.all()
        
        return False
