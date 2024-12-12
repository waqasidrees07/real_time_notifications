import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from notification_app.models import Notification

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f"user_{self.scope['user'].id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Raw data received: {text_data}")
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return

        message = data.get('message', 'No message provided')
        await self.create_notification(message)
        await self.send(text_data=json.dumps({'message': 'Notification created successfully'}))

    @staticmethod
    async def create_notification(message):
        from asgiref.sync import sync_to_async
        return await sync_to_async(Notification.objects.create)(message=message)
