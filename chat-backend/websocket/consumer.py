from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PingConsumer(AsyncJsonWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        # self.group_name = group_name
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        await self.send_json(
            {"type": "init", "message": f"conected to: {self.room_group_name}"}
        )

    async def receive_json(self, content, **kwargs):
        credentials = content.get("credentials", {})
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
