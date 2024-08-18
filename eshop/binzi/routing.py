from django.urls import re_path  # re_path is more common for WebSockets
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<recipient_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
