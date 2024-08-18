import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from binzi.routing import websocket_urlpatterns  # Import WebSocket URL patterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eshop.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # WebSocket requests
        )
    ),
})
