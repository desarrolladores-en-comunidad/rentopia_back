"""
ASGI config for rentopia project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from apps.messaging.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentopia.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
            URLRouter([
                re_path(r'ws/api/messages/(?P<property_id>[^/]+)/$', ChatConsumer.as_asgi()),
            ])
    ),
})