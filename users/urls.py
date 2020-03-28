# users/urls.py
from django.urls import path
from .views import does_username_exists, ajax_login, ajax_register
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('ajax/username_exist/', does_username_exists, name='validate_username_l'),
    path('ajax/login_api', ajax_login),
    path('ajax/register_api', ajax_register),
    path('rest_api/token_auth_login', obtain_auth_token, name="login_auth_token"),
]
