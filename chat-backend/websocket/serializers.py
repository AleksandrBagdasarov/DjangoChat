from typing import Union

from api.actions.chat.messages.serializers import MessageSerializer
from api.models import Message
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from rest_framework import serializers
from websocket.actions import (
    add_message_to_chat,
    add_scheduled_message,
    chat_exist,
    set_scheduled_message_executed,
)


class ReceiveJsonTypes:
    # Regular message
    CHAT_MESSAGE = "chat_message"
    # User Sent Scheduled message to WS
    SCHEDULED_MESSAGE = "scheduled_message"
    # Refresh Access token
    REFRESH = "refresh"
    # Scheduler process user scheduled message
    SCHEDULER = "scheduler"

    choices = (
        (CHAT_MESSAGE, CHAT_MESSAGE),
        (SCHEDULED_MESSAGE, SCHEDULED_MESSAGE),
        (REFRESH, REFRESH),
        (SCHEDULER, SCHEDULER),
    )


class ReceiveJsonTypesSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=ReceiveJsonTypes.choices, allow_null=False
    )


class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=512, allow_null=False, allow_blank=False
    )

    async def process(self, chat_consumer):
        message_obj = await add_message_to_chat(
            user=chat_consumer.user,
            chat=chat_consumer.chat,
            text=self.data["message"],
        )
        message_obj_serializer = MessageSerializer(
            message_obj, context={"user_id": chat_consumer.user.id}
        )
        await chat_consumer.channel_layer.group_send(
            chat_consumer.room_group_name,
            {
                "type": "chat_message",
                "message_obj": message_obj_serializer.data,
                "user_id": chat_consumer.user.id,
            },
        )


class SchedulerProcessSerializer(ChatMessageSerializer):
    scheduled_message_id = serializers.IntegerField(allow_null=False)

    async def process(self, chat_consumer):
        await super().process(chat_consumer)
        await set_scheduled_message_executed(self.data["scheduled_message_id"])


class ScheduledMessageSerializer(ChatMessageSerializer):
    execute_at = serializers.DateTimeField(allow_null=False)

    async def process(self, chat_consumer):
        await add_scheduled_message(
            user=chat_consumer.user,
            chat=chat_consumer.chat,
            text=self.data["message"],
            execute_at=self.data["execute_at"],
        )


def get_serializer_class(type: str):
    serializers = {
        ReceiveJsonTypes.CHAT_MESSAGE: ChatMessageSerializer,
        ReceiveJsonTypes.SCHEDULED_MESSAGE: ScheduledMessageSerializer,
        ReceiveJsonTypes.SCHEDULER: SchedulerProcessSerializer,
    }
    return serializers[type]
