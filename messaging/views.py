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
    if request.is_ajax():
        if request.GET.get('receiver') == "":
            messages.error(request, "Select a conversation, please")
            return HttpResponseRedirect('/messaging/inbox/')
        else:
            receiver = get_object_or_404(User, username=request.GET.get('receiver'))
            if request.method == 'GET':
                message = Message(sender=request.user,
                                  receiver=receiver,
                                  msg_content=request.GET.get('msg'),
                                  created_at=datetime.datetime.now())
                message.save()
                return HttpResponse(json.dumps("success", cls=DjangoJSONEncoder), content_type='application/json')
    else:
        return HttpResponseRedirect('/messaging/inbox/')


@login_required
def inbox(request):
    user_last = dict()
    if request.method == 'POST':
        if request.POST.get('username'):
            add_user = get_object_or_404(User, username=request.POST.get('username'))
            user_last[datetime.datetime.now()] = {"user": add_user, "message": ""}
    message_list = Message.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
    if message_list:
        user_conversations = set()
        for message in message_list:
            user_conversations.add(message.receiver)
            user_conversations.add(message.sender)
            message.read = True
            message.save()
        user_conversations.remove(request.user)
        for user in user_conversations:
            last_message = Message.objects.filter((Q(receiver=request.user) & Q(sender=user)) | (Q(receiver=user) & Q(sender=request.user))).order_by('-created_at')[0]
            user_last[last_message.created_at] = {"user": user, "message": last_message}
    user_last = sorted(user_last.items(), key=lambda t: t[0], reverse=True)
    return render(request, 'messaging/inbox.html', {'user_last': user_last,
                                                    'MEDIA_URL': MEDIA_URL})


@login_required
def show_messages(request):
    if request.is_ajax():
        username = request.GET.get('user')
        user = get_object_or_404(User, username=username)
        conversation = Message.objects.filter(
            (Q(receiver=request.user) & Q(sender=user)) | (Q(receiver=user) & Q(sender=request.user))).order_by(
            '-created_at')[:50]
        messages = list()
        for message in conversation:
            if message.sender == request.user:
                messages.append({"user": "me", "message": message.msg_content, "created_at": message.created_at})
            else:
                messages.append({"user": "you", "message": message.msg_content, "created_at": message.created_at})
        return HttpResponse(json.dumps(messages, cls=DjangoJSONEncoder), content_type='application/json')

