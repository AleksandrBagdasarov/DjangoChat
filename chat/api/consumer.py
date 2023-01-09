from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PingConsumer(AsyncJsonWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        await self.accept()
        await self.send_json({"message": "conected"})

    async def receive_json(self, content, **kwargs):
        await self.send_json(
            {
                "type": "websocket.send",
                "text": "pong",
            }
        )
