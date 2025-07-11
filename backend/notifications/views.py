import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification


@csrf_exempt
@require_http_methods(["POST"])
def send_notification(request):
    """
    Endpoint: POST /api/notifications/send/
    Description: Send an email and push notification for a booking.
    Required JSON fields: service, recipient
    """
    try:
        data = json.loads(request.body)
        service = data.get("service")
        recipient = data.get("recipient")

        if not all([service, recipient]):
            return JsonResponse({"error": "Missing 'service' or 'recipient' field."}, status=400)

        title = "Booking Confirmation"
        message = f"Dear customer, your booking for {service} has been successfully received. Thank you for choosing us!"

        # Send email
        send_mail(
            subject=title,
            message=message,
            from_email="cwash3001@gmail.com",
            recipient_list=[recipient],
            fail_silently=False,
        )

        # Save to DB
        notification = Notification.objects.create(
            title=title,
            message=message,
            recipient_email=recipient,
            sent=True,
            sent_at=timezone.now(),
        )

        # Send to WebSocket group
        tenant_id = "123"  # This should match the tenant ID used in WebSocket URL
        group_name = f"tenant_{tenant_id}_notifications"

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",  # Must match method in consumer
                "message": message,
            }
        )

        return JsonResponse({
            "status": "Notification sent and saved.",
            "notification_id": notification.id
        }, status=201)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def get_notifications(request):
    """
    Endpoint: GET /api/notifications/
    Description: Retrieve all notifications. Optionally filter by ?recipient=email
    """
    recipient = request.GET.get("recipient")
    if recipient:
        notifications = Notification.objects.filter(recipient_email=recipient)
    else:
        notifications = Notification.objects.all()

    data = list(notifications.values())
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def get_notification_by_id(request, notification_id):
    """
    Endpoint: GET /api/notifications/<id>/
    Description: Retrieve a specific notification by ID.
    """
    notification = get_object_or_404(Notification, id=notification_id)
    return JsonResponse({
        "id": notification.id,
        "title": notification.title,
        "message": notification.message,
        "recipient_email": notification.recipient_email,
        "sent": notification.sent,
        "sent_at": notification.sent_at,
    }, status=200)

