# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ajax/validate_username_l/', views.validate_username_l, name='validate_username_l'),
    path('ajax/login_api', views.ajax_login)
]
