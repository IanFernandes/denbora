from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^show_messages/$', views.show_messages, name='show_messages'),
]
