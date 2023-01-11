from api.models import Chat
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        self.user = self.scope["user"]
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        chat = await sync_to_async(Chat.objects.filter, thread_sensitive=True)(
            id=self.chat_id
        )
        if not chat:
            await self.disconnect(404)
        self.room_group_name = "chat_%s" % self.chat_id
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        await self.send_json(
            {"type": "init", "message": f"conected to: {self.room_group_name}"}
        )

    async def receive_json(self, content, **kwargs):
        # credentials = content.get("credentials", {})
        message = content.get("message", "")
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
        await self.send_json({"type": "message", "message": message})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send_json({"message": message})
