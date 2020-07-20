# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat_test.routing
import games.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            # chat_test.routing.websocket_urlpatterns,
            games.routing.websocket_urlpatterns
        )
    ),
})