from django.conf.urls import url

from . import views


app_name = 'shopping'

urlpatterns = [
    # ex: /shopping/
    url(r'^$', views.index, name='index'),
    url(r'^korea/$', views.korea, name='korea'),
    url(r'^overseas/$', views.overseas, name='overseas'),
    url(r'^collect/$', views.collect, name='collect'),
]