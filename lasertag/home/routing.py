from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/$', consumers.GameActionConsumer.as_asgi()),
    re_path(r'ws/guns/$', consumers.LasergunConsumer.as_asgi()),
    re_path(r'ws/control/$', consumers.GameControlConsumer.as_asgi()),
]