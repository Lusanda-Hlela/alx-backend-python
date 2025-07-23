from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants in a conversation
    to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Support GET, POST, PUT, PATCH, DELETE
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            conversation = getattr(obj, 'conversation', None)
            if conversation and request.user in conversation.participants.all():
                return True
            return False

        return False
