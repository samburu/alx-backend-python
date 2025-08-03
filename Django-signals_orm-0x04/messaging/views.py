from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User


@login_required
def delete_user(request):
    user = request.user
    logout(request)  # log them out first
    user.delete()
    return redirect("home")  # redirect to home page or login page


@login_required
def inbox(request):
    messages = Message.objects.filter(
        receiver=request.user
    ).select_related("sender", "receiver").prefetch_related("replies")
    return render(request, "messaging/inbox.html", {"messages": messages})


@login_required
def sent_messages(request):
    messages = Message.objects.filter(
        sender=request.user
    ).select_related("receiver")
    return render(request, "messaging/sent_messages.html", {"messages": messages})