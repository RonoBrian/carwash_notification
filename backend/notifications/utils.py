from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def trigger_notification(tenant_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"tenant_{tenant_id}_notifications",
        {
            "type": "send_notification",
            "message": message,
        }
    )
