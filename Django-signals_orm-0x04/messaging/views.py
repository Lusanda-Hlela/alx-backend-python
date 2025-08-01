from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch
from django.views.decorators.cache import cache_page


@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')  # Redirect to home or login page after deletion


@login_required
def threaded_messages_view(request):
    messages = (
        Message.objects.filter(sender=request.user, parent_message=None)
        .select_related("receiver")
        .prefetch_related("replies")
    )

    context = {"messages": messages}
    return render(request, "messaging/threaded_messages.html", context)


@login_required
def unread_messages_view(request):
    # ✅ Use the manager with the exact method name
    unread_msgs = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')

    return render(
        request, "messaging/unread_messages.html", {"unread_messages": unread_msgs}
    )

@cache_page(60)  # Cache for 60 seconds
def conversation_view(request, user_id):
    messages = Message.objects.filter(sender_id=user_id)
    return render(request, 'messaging/conversation.html', {'messages': messages})
