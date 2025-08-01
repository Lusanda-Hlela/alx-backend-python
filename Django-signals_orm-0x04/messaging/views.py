from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Prefetch

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
    unread_msgs = Message.unread.for_user(request.user)

    context = {"unread_messages": unread_msgs}
    return render(request, "messaging/unread_messages.html", context)
