from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from messaging.forms import MessageForm
from messaging.models import Message
import datetime


@login_required
def send_message(request, username):
    message_form = {}
    receiver = get_object_or_404(User, username=username)
    if request.method == 'GET':
        message_form = MessageForm()
    elif request.method == 'POST':
        message_form = MessageForm(request.POST, request.FILES)
        if message_form.is_valid():
            message = Message(sender=request.user,
                              receiver=receiver,
                              title=message_form.cleaned_data['title'],
                              msg_content=message_form.cleaned_data['msg_content'],
                              created_at=datetime.datetime.now())
            message.save()
            return HttpResponseRedirect('/messaging/email_sent/')
    return render(request, 'messaging/send_message.html', {'receiver': receiver,
                                                           'message_form': message_form})


@login_required
def email_sent(request):
    return HttpResponse("Your message has been sent")


@login_required
def inbox(request):
    message_list = Message.objects.filter(receiver=request.user)
    for message in message_list:
        message.read = True
        message.save()
    return render(request, 'messaging/inbox.html', {'message_list': message_list})


@login_required
def sent_box(request):
    message_list = Message.objects.filter(sender=request.user)
    return render(request, 'messaging/sent_box.html', {'message_list': message_list})
