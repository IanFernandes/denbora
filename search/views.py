from django.shortcuts import render, HttpResponse
from profiles.models import Skill
from accounts.models import User
import json
from django.db import connection
from denbora_project.settings import MEDIA_URL
from messaging.models import Message


def index(request):
    if request.user.is_authenticated:
        message_unread = Message.objects.filter(receiver=request.user, read=False).count()
    else:
        message_unread = ""
    return render(request, 'search/index.html', {'message_unread': message_unread})


def search(request):
    if request.user.is_authenticated:
        message_unread = Message.objects.filter(receiver=request.user, read=False).count()
    else:
        message_unread = ""
    user_data = list()
    search_data = dict()
    if request.method == 'POST':
        skill = Skill.objects.get(pk=request.POST['skillid'])
        search_data['skill'] = skill.name
        search_data['location'] = request.POST['city']
        cursor = connection.cursor()
        lat = request.POST['lat']
        lon = request.POST['lon']
        cursor.execute("""SELECT id, (
                        6371 * acos( cos( radians(%s) ) * cos( radians( lat ) ) *
                        cos( radians( lon ) - radians(%s) ) + sin( radians(%s) ) *
                        sin( radians( lat ) ) ) )
                        AS distance FROM profiles_city HAVING distance < 25
                        ORDER BY distance LIMIT 0 , 20;""", (lat, lon, lat))
        city_ids = [row[0] for row in cursor.fetchall()]
        users = User.objects.filter(city_id__in=city_ids)
        for user in users:
            if user.userskill_set.filter(skill=skill).exists():
                user_data.append(user)
    return render(request, 'search/search.html', {'user_data': user_data,
                                                  'MEDIA_URL': MEDIA_URL,
                                                  'search_data': search_data,
                                                  'message_unread': message_unread})


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
