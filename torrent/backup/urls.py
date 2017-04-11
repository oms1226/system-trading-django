from django.conf.urls import url

from . import views

app_name = 'torrent'

urlpatterns = [
    # ex: /torrent/
    url(r'^$', views.index, name='index'),
    # ex: /torrent/backup/
    url(r'^collect/$', views.collect, name='collect'),
    url(r'^rss/$', views.rss, name='rss'),
    url(r'^showrss/$', views.showrss, name='rss'),
    # url(r'^rss/$', RssFeed()),
    # url(r'^rss/item/(?P<magnet_id>\d+)/', views.item, name='item'),
    url(r'^rss/item/(?P<item_id>\d+)', views.item, name='item'),

]