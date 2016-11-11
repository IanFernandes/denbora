from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^send_message/username=(?P<username>.*)/$', views.send_message, name='send_message'),
    url(r'^email_sent/$', views.email_sent, name='email_sent'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^sent_box/$', views.sent_box, name='sent_box'),
]
