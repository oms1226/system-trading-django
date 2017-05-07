from django.conf.urls import url

from . import views


app_name = 'stock'

urlpatterns = [
    # ex: /stock/
    url(r'^$', views.index, name='index'),
    url(r'^a/$', views.analyze, name='analyze'),
    url(r'^c/$', views.collect, name='collect'),
    url(r'^v/(?P<strategy>.+)/(?P<code>.+)/', views.view, name='view'),
    # /stock/s/ra5/A001525
    url(r'^s/(?P<strategy>.+)/(?P<code>.+)/', views.simulate, name='simulate'),
]