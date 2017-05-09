from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views


app_name = 'manager'

urlpatterns = [
    # ex: /manager/
    url(r'^$', views.index, name='index'),
    url(r'^a/$', views.analyze, name='analyze'),
    url(r'^c/$', views.collect, name='collect'),
    # url(r'^v/(?P<strategy>.+)/(?P<code>.+)/', views.view, name='view'),
    # /manager/s/ra5/A001525
    # url(r'^s/(?P<strategy>.+)/(?P<code>.+)/', views.simulate, name='simulate'),
    url(r'^s/(?P<code>.+)/(?P<buy_code>.+)/(?P<sell_code>.+)/(?P<start_money>.+)/', views.simulate, name='simulate'),

    url(r'^add/', views.add_stock, name='add')

]

urlpatterns += staticfiles_urlpatterns()