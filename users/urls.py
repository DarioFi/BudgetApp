# users/urls.py
from django.urls import path
from django.views.generic import TemplateView

from .views import does_username_exists, ajax_login, ajax_register, is_authenticated, login_request
from rest_framework.authtoken.views import obtain_auth_token


# /users/

urlpatterns = [
    path('ajax/username_exist/', does_username_exists, name='validate_username_l'),
    path('ajax/login_api', ajax_login),
    path('ajax/register_api', ajax_register),
    path('rest_api/token_auth_login', obtain_auth_token, name="login_auth_token"),
    path('rest_api/auth_check', is_authenticated),
    path('login/', login_request, name="login"),
]
