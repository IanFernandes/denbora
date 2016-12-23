from profiles.forms import EditForm
from profiles.models import City


def load_edit_form(request):
    return EditForm(initial={'first_name': request.user.first_name,
                             'last_name': request.user.last_name,
                             'email': request.user.email,
                             'city': request.user.city.complete_location,
                             'city_name': request.user.city.name,
                             'lat': request.user.city.lat,
                             'lon': request.user.city.lon,
                             'country_code': request.user.city.country_code,
                             'description': request.user.description})


def manage_city(edit_form):
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
    return city


def update_account(user_data, edit_form):
    if edit_form.cleaned_data['city']:
        city = manage_city(edit_form)
        user_data.city = city
    if edit_form.cleaned_data['avatar']:
        user_data.avatar = edit_form.cleaned_data['avatar']
    user_data.first_name = edit_form.cleaned_data['first_name']
    user_data.last_name = edit_form.cleaned_data['last_name']
    user_data.email = edit_form.cleaned_data['email']
    user_data.description = edit_form.cleaned_data['description']
    user_data.save()
