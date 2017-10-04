from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^createAlbum/(?P<id>\d+)$', views.createAlbum),
    url(r'^deleteAlbum/(?P<id>\d+)$', views.deleteAlbum),
]
