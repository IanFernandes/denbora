from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^activate/q=(?P<data>.*)/$', views.activate, name='activate'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^logged_out/$', views.logged_out, name='logged_out'),
]
