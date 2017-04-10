from django.conf.urls import url

from . import views
from .views import RssFeed

app_name = 'torrent'

urlpatterns = [
    # ex: /torrent/
    url(r'^$', views.index, name='index'),
    # ex: /torrent/site/
    url(r'^collect/$', views.collect, name='collect'),
    # url(r'^rss/$', views.rss, name='rss'),
    url(r'^rss/$', RssFeed()),
]