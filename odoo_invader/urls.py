from django.urls import path
from django.conf.urls import url
from django.urls import re_path
from . import views

app_name = 'odoo_invader'
urlpatterns = [

    # path('ajax_view', views.my_ajax_view, name='ajax_view'),
    #url(r'^odoo_api/$', views.OdooApi.as_view(), name="odoo_api"),
    path('odoo_api/<path:service_path>', views.OdooApi.as_view(), name="odoo_api"),
]