from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils.dateparse import parse_datetime
from websocket.actions import (
    add_message_to_chat,
    add_scheduled_message,
    chat_exist,
    set_scheduled_message_executed,
)
from websocket.serializers import (
    ChatMessageSerializer,
    MessageSerializer,
    ReceiveJsonTypes,
    ReceiveJsonTypesSerializer,
    SchedulerProcessSerializer,
    get_serializer_class,
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
        # check correct message type
        type_serializer = ReceiveJsonTypesSerializer(
            data={"type": content.get("type", "")}
        )
        type_serializer.is_valid(raise_exception=True)
        # todo should i return response about invalid type??

        serializer_class = get_serializer_class(type_serializer.data["type"])
        serializer = serializer_class(data=content)
        serializer.is_valid(raise_exception=True)
        await serializer.process(chat_consumer=self)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def chat_message(self, event):
        message_obj = event["message_obj"]
        if self.user.id == event["user_id"]:
            message_obj["owner"] = True
        await self.send_json(message_obj)
