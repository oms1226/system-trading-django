from django.conf.urls import url

from . import views


app_name = 'stock'

urlpatterns = [
    # ex: /stock/
    #url(r'^$', views.index, name='index'),
    url(r'^analyze/$', views.analyze, name='analyze'),
    #url(r'^sell/$', views.sell, name='sell'),
]