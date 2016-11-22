from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profiles.forms import EditForm, AddSkillForm
from profiles.models import City
from django.http import HttpResponseRedirect, HttpResponse
from denbora_project.settings import MEDIA_URL
from profiles.models import Skill, SkillCategory, UserSkill
from messaging.models import Message
from django.contrib import messages


@login_required
def user_data(request):
    userskills = request.user.userskill_set.all()
    message_unread = Message.objects.filter(receiver=request.user, read=False).count()
    return render(request, 'profiles/user_data.html', {'user_skills': userskills,
                                                       'MEDIA_URL': MEDIA_URL,
                                                       'message_unread': message_unread})


@login_required
def edit(request):
    message_unread = Message.objects.filter(receiver=request.user, read=False).count()
    edit_form = {}
    if request.method == 'GET':
        edit_form = EditForm(initial={'first_name': request.user.first_name,
                                      'last_name': request.user.last_name,
                                      'email': request.user.email,
                                      'city': request.user.city.complete_location,
                                      'city_name': request.user.city.name,
                                      'lat': request.user.city.lat,
                                      'lon': request.user.city.lon,
                                      'country_code': request.user.city.country_code,
                                      'description': request.user.description})

    elif request.method == 'POST':
        edit_form = EditForm(request.POST, request.FILES)
        if edit_form.is_valid():
            if edit_form.cleaned_data['city']:
                name = edit_form.cleaned_data['city_name']
                lat = float(edit_form.cleaned_data['lat'])
                lon = float(edit_form.cleaned_data['lon'])
                if not City.objects.filter(name=name, lat=lat, lon=lon).exists():
                    complete_location = edit_form.cleaned_data['city']
                    country_code = edit_form.cleaned_data['country_code']
                    city = City(name=name,
                                complete_location=complete_location,
                                country_code=country_code,
                                lat=lat,
                                lon=lon)
                    city.save()
                else:
                    city = City.objects.get(name=name, lat=lat, lon=lon)
                request.user.city = city
            else:
                request.user.city_id = 1

            if edit_form.cleaned_data['avatar']:
                request.user.avatar = edit_form.cleaned_data['avatar']
            request.user.first_name = edit_form.cleaned_data['first_name']
            request.user.last_name = edit_form.cleaned_data['last_name']
            request.user.email = edit_form.cleaned_data['email']
            request.user.description = edit_form.cleaned_data['description']
            request.user.save()
            messages.success(request, "Your data has been stored properly")
            return HttpResponseRedirect('/profiles')
    return render(request, 'profiles/edit.html', {'edit_form': edit_form,
                                                  'message_unread': message_unread,
                                                  'MEDIA_URL': MEDIA_URL})


@login_required
def add_skill(request):
    message_unread = Message.objects.filter(receiver=request.user, read=False).count()
    if request.method == 'POST':
        add_skill_form = AddSkillForm(request.POST)
        if add_skill_form.is_valid():
            category = SkillCategory.objects.get(id=add_skill_form.cleaned_data['category'])
            skill_name = add_skill_form.cleaned_data['skill_name']
            desc = add_skill_form.cleaned_data['desc']
            if Skill.objects.filter(name=skill_name, category=category, desc=desc).exists():
                skill = Skill.objects.get(name=skill_name, category=category, desc=desc)
            else:
                skill = Skill(name=add_skill_form.cleaned_data['skill_name'],
                              category=category,
                              desc=add_skill_form.cleaned_data['desc'])
            if UserSkill.objects.filter(user=request.user, skill=skill).exists():
                messages.error(request, "This skill is already added")

            else:
                skill.save()
                user_skill = UserSkill(user=request.user,
                                       skill=skill)
                user_skill.save()
                messages.success(request, "Skill correctly added")
                return HttpResponseRedirect('/profiles')
    else:
        add_skill_form = AddSkillForm()
    return render(request, 'profiles/add_skill.html', {'add_skill_form': add_skill_form,
                                                       'MEDIA_URL': MEDIA_URL,
                                                       'message_unread': message_unread,})
