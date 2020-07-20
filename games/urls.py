from django.urls import path, include
from .views import *

urlpatterns = [
    path('room/<int:room_id>', open_room)  # todo: deprecate room_id and use the slug
]