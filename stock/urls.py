from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from .v1 import views as v1


app_name = 'stock'

urlpatterns = [
    # ex: /manager/
    url(r'^$', views.index, name='index'),
    url(r'^c/$', views.collect, name='collect'),
    # url(r'^v/(?P<strategy>.+)/(?P<code>.+)/', views.view, name='view'),
    # /manager/s/ra5/A001525
    # url(r'^s/(?P<strategy>.+)/(?P<code>.+)/', views.simulate, name='simulate'),
    # url(r'^s/(?P<stock_code>.+)/(?P<buy_code>.+)/(?P<sell_code>.+)/(?P<start_money>.+)/', views.simulate_data, name='simulate_data'),
    url(r'^add/', views.add_stock, name='add'),
    url(r'^v1/simulate/data/$', v1.simulate_data, name='v1_simulate_data'),
    url(r'^simulate/(?P<code_type>.+)/$', views.simulate_type, name='simulate_type'),

]

urlpatterns += staticfiles_urlpatterns()