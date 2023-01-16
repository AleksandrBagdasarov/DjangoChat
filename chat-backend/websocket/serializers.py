from api.actions.chat.messages.serializers import MessageSerializer
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from websocket.actions import (
    add_message_to_chat,
    add_scheduled_message,
    set_scheduled_message_executed,
)


class ReceiveJsonTypes:
    # Regular message
    CHAT_MESSAGE = "chat_message"
    # Anonymous message
    ANONYMOUS_MESSAGE = "anonymous_message"
    # User Sent Scheduled message to WS
    SCHEDULED_MESSAGE = "scheduled_message"
    # Refresh Access token
    REFRESH = "refresh"
    # Scheduler process user scheduled message
    SCHEDULER = "scheduler"

    choices = (
        (CHAT_MESSAGE, CHAT_MESSAGE),
        (ANONYMOUS_MESSAGE, ANONYMOUS_MESSAGE),
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
    anonymous = serializers.BooleanField(default=False, allow_null=True)

    async def process(self, chat_consumer):
        if self.data["anonymous"]:
            user = None
            user_id = None
        else:
            user = chat_consumer.user
            user_id = chat_consumer.user.id

        message_obj = await add_message_to_chat(
            user=user,
            chat=chat_consumer.chat,
            text=self.data["message"],
        )
        message_obj_serializer = MessageSerializer(
            message_obj, context={"user_id": user_id}
        )
        await chat_consumer.channel_layer.group_send(
            chat_consumer.room_group_name,
            {
                "type": "chat_message",
                "message_obj": message_obj_serializer.data,
                "user_id": user_id,
            },
        )


class SchedulerProcessSerializer(ChatMessageSerializer):
    scheduled_message_id = serializers.IntegerField(allow_null=False)

    async def process(self, chat_consumer, anonymous=False):
        await super().process(chat_consumer)
        await set_scheduled_message_executed(self.data["scheduled_message_id"])


class ScheduledMessageSerializer(ChatMessageSerializer):
    execute_at = serializers.DateTimeField(allow_null=False)

    async def process(self, chat_consumer, anonymous=False):
        if self.data["anonymous"]:
            user = None
        else:
            user = chat_consumer.user

        await add_scheduled_message(
            user=user,
            chat=chat_consumer.chat,
            text=self.data["message"],
            execute_at=self.data["execute_at"],
        )


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=512)

    async def process(self, chat_consumer):
        refresh = RefreshToken(token=self.data["refresh"])
        access = refresh.access_token
        await chat_consumer.send_json(
            {
                "type": ReceiveJsonTypes.REFRESH,
                "refresh": str(refresh),
                "access": str(access),
            }
        )


def get_serializer_class(type: str):
    serializers = {
        ReceiveJsonTypes.CHAT_MESSAGE: ChatMessageSerializer,
        ReceiveJsonTypes.SCHEDULED_MESSAGE: ScheduledMessageSerializer,
        ReceiveJsonTypes.SCHEDULER: SchedulerProcessSerializer,
        ReceiveJsonTypes.REFRESH: RefreshTokenSerializer,
    }
    return serializers[type]
