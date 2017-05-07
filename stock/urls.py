from django.conf.urls import url

from . import views


app_name = 'stock'

urlpatterns = [
    # ex: /stock/
    url(r'^$', views.index, name='index'),
    url(r'^a/$', views.analyze, name='analyze'),
    url(r'^v/(?P<code>.+)/', views.view, name='view'),
    url(r'^c/$', views.collect, name='collect'),
]