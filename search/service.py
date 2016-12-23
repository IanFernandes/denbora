from django.db import connection
from accounts.models import User


def get_users(lat, lon, skill):
    datas = list()
    cursor = connection.cursor()
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
            skill_data = user.userskill_set.get(skill=skill)
            datas.append({'user': user, 'skill': skill_data})
    return datas


def load_search_data(request_data):
    search_data = dict()
    search_data['skill'] = request_data['skill']
    search_data['location'] = request_data['city']
    search_data['lat'] = request_data['lat']
    search_data['lon'] = request_data['lon']
    return search_data



