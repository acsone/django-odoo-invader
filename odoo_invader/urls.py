# Copyright 2018 ACSONE SA/NV
from django.urls import path
from . import views

app_name = 'odoo_invader'
urlpatterns = [
    path('odoo_api/<path:service_path>',
         views.OdooApi.as_view(),
         name="odoo_api"),
]
