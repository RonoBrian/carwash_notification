# notifications/urls.py
from django.urls import path
from .views import send_notification, get_notifications, get_notification_by_id


urlpatterns = [
    path('notifications/', get_notifications, name='get_notifications'),
    path('notifications/<int:notification_id>/', get_notification_by_id, name='get_notification_by_id'),
    path('notifications/send/', send_notification, name='send_notification'),
]
