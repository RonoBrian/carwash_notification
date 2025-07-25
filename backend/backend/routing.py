# backend/routing.py

from django.urls import re_path
from notifications.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/(?P<tenant_id>\w+)/$", NotificationConsumer.as_asgi()),
]
