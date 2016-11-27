from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from messaging.models import Message
import datetime
from django.db.models import Q
from denbora_project.settings import MEDIA_URL
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages


@login_required
def send_message(request):
    if request.POST.get('receiver') == "":
        messages.error(request, "Select a conversation, please")
        return HttpResponseRedirect('/messaging/inbox/')
    else:
        receiver = get_object_or_404(User, username=request.POST.get('receiver'))
        if request.method == 'POST':
            message = Message(sender=request.user,
                              receiver=receiver,
                              msg_content=request.POST.get('msg_content'),
                              created_at=datetime.datetime.now())
            message.save()
            messages.success(request, "Your message has been sent")
            return HttpResponseRedirect('/messaging/inbox/')
        else:
            return HttpResponseRedirect('/messaging/inbox/')


@login_required
def inbox(request):
    message_list = Message.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
    user_conversations = set()
    for message in message_list:
        user_conversations.add(message.receiver)
        user_conversations.add(message.sender)
        message.read = True
        message.save()
    user_conversations.remove(request.user)
    user_last = dict()
    for user in user_conversations:
        last_message = Message.objects.filter((Q(receiver=request.user) & Q(sender=user)) | (Q(receiver=user) & Q(sender=request.user))).order_by('-created_at')[0]
        user_last[user] = last_message
    return render(request, 'messaging/inbox.html', {'user_last': user_last,
                                                    'MEDIA_URL': MEDIA_URL})


@login_required
def show_messages(request):
    if request.is_ajax():
        username = request.GET.get('user')
        user = get_object_or_404(User, username=username)
        conversation = Message.objects.filter(
            (Q(receiver=request.user) & Q(sender=user)) | (Q(receiver=user) & Q(sender=request.user))).order_by(
            '-created_at')
        messages = list()
        for message in conversation:
            if message.sender == request.user:
                messages.append({"user": "me", "message": message.msg_content, "created_at": message.created_at})
            else:
                messages.append({"user": "you", "message": message.msg_content, "created_at": message.created_at})
        return HttpResponse(json.dumps(messages, cls=DjangoJSONEncoder), content_type='application/json')

