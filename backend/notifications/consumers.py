# notifications/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.tenant_id = self.scope["url_route"]["kwargs"]["tenant_id"]
        self.group_name = f"{self.tenant_id}_notifications"

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        # Optional: Notify client of successful connection
        await self.send(text_data=json.dumps({
            "message": f"🔗 Connected to group {self.group_name}"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Optional: Echo back or ignore
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            "message": f"📨 You sent: {data.get('message', '')}"
        }))

    async def send_notification(self, event):
        message = event.get("message", "")
        print("📨 send_notification triggered with:", event)
        await self.send(text_data=json.dumps({
            "message": message
        }))
