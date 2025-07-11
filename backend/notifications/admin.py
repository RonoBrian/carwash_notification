from django.contrib import admin
from .models import Notification  # Your actual model

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "recipient_email", "sent", "sent_at")
    search_fields = ("title", "recipient_email")
