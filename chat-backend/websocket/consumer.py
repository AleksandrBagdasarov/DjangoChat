from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.dateparse import parse_datetime
from websocket.actions import (
    add_message_to_chat,
    add_scheduled_message,
    chat_exist,
    set_scheduled_message_executed,
)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]

        # todo error if chat does not exist
        self.chat = await chat_exist(self.chat_id)

        # user from query middleware
        # example: ws://localhost:8888/ws/1/?access=<JWToken>
        self.user = self.scope["user"]

        self.room_group_name = "chat_%s" % self.chat_id
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def receive_json(self, content, **kwargs):
        message_text = content.get("message", "")
        scheduled_message = content.get("scheduled_message", False)
        scheduler = content.get("scheduler")

        if scheduled_message:
            execute_at = parse_datetime(content["execute_at"])
            await add_scheduled_message(
                user=self.user,
                chat=self.chat,
                text=message_text,
                execute_at=execute_at,
            )
        else:
            result = await add_message_to_chat(
                user=self.user, chat=self.chat, text=message_text
            )

            # !important
            # <message_obj> should have same keys as
            # api GET messages serializer
            message_obj = {
                "id": result.id,
                "owner": False,
                "username": self.user.username,
                "user": self.user.id,
                "chat": self.chat.id,
                "text": message_text,
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            }

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message_obj": message_obj,
                    "user_id": self.user.id,
                },
            )
            # If this message from scheduler
            # must provide "scheduled_message_id" key
            if scheduler:
                scheduled_message_id = content.get("scheduled_message_id")
                await set_scheduled_message_executed(scheduled_message_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def chat_message(self, event):
        message_obj = event["message_obj"]
        if self.user.id == event["user_id"]:
            message_obj["owner"] = True
        await self.send_json(message_obj)
