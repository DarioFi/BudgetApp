# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ajax/username_exist/', views.does_username_exists, name='validate_username_l'),
    path('ajax/login_api', views.ajax_login),
    path('ajax/register_api', views.ajax_register),
]
