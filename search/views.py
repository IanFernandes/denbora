import json

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from denbora_project.settings import MEDIA_URL
from messaging.models import Message
from profiles.models import Skill
from search.service import get_users, load_search_data


def index(request):
    if request.user.is_authenticated:
        message_unread = Message.objects.filter(receiver=request.user, read=False).count()
    else:
        message_unread = ""
    return render(request, 'search/index.html', {'message_unread': message_unread})


def search(request):
    if request.method == 'POST':
        try:
            skill = Skill.objects.get(name=request.POST['skill'])
        except ObjectDoesNotExist:
            messages.info(request, request.POST['skill'] + " Skill does not Exist")
            return HttpResponseRedirect('/')
        search_data = load_search_data(request.POST)
        users_data = get_users(request.POST['lat'], request.POST['lon'], skill)
        if request.user.is_authenticated:
            message_unread = Message.objects.filter(receiver=request.user, read=False).count()
        else:
            message_unread = ""
        return render(request, 'search/search.html', {'datas': users_data,
                                                      'MEDIA_URL': MEDIA_URL,
                                                      'search_data': search_data,
                                                      'message_unread': message_unread})
    else:
        return HttpResponseRedirect('/')


def autocomplete_skill(request):
    data_json = {}
    if request.is_ajax:
        search = request.GET.get('term', '')
        skills = Skill.objects.filter(name__icontains=search)
        results = []
        for skill in skills:
            skill_json = dict()
            skill_json['label'] = skill.name
            skill_json['value'] = skill.name
            skill_json['id'] = skill.id
            skill_json['cate'] = skill.category.name
            results.append(skill_json)
        data_json = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data_json, mimetype)
