from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sublease.models import Sublease
from .models import Conversation, Message
from django.db.models import Q

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(user1=request.user) | \
                    Conversation.objects.filter(user2=request.user)
    return render(request, "messaging/inbox.html", {"conversations": conversations})


@login_required
def start_conversation(request, sublease_id):
    sublease = get_object_or_404(Sublease, pk=sublease_id)
    other_user = sublease.user

    if other_user == request.user:
        return redirect("message-inbox")

    convo = Conversation.objects.filter(
        Q(user1=request.user, user2=other_user) |
        Q(user1=other_user, user2=request.user)
    ).first()

    if convo is None:
        convo = Conversation.objects.create(user1=request.user, user2=other_user)

    return redirect("message-thread", conversation_id=convo.id)


@login_required
def conversation_view(request, conversation_id):
    convo = get_object_or_404(Conversation, id=conversation_id)

    if request.user not in [convo.user1, convo.user2]:
        return redirect("message-inbox")

    if request.method == "POST":
        text = request.POST.get("text")
        if text:
            Message.objects.create(
                conversation=convo,
                sender=request.user,
                text=text
            )
            return redirect("message-thread", conversation_id=conversation_id)

    messages = convo.messaging.order_by("timestamp")

    conversations = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)

    return render(request,"messaging/thread.html",
                  {"conversation": convo, "messaging": messages, "conversations": conversations,})