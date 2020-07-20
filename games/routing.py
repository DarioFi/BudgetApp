# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'wss/games/room/(?P<room_id>\w+)/$', consumers.GameConsumer),
]