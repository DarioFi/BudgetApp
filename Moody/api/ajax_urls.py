from django.urls import path
from Moody.api.ajax import *

urlpatterns = [
    path("moody_data", get_moody_data),
    path("check_if_exists", check_if_moody_exists),
    path("generate_record", generate_moody_user_if_not_exist_post)
]
