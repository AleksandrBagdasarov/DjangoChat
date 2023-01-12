from datetime import datetime

from api.models import Chat, Message, ScheduledMessage, User, UserToChat
from channels.db import database_sync_to_async


@database_sync_to_async
def chat_exist(chat_id) -> Chat or None:
    try:
        return Chat.objects.get(id=chat_id)
    except Exception:
        return


@database_sync_to_async
def add_message_to_chat(user: User, chat: Chat, text: str):
    Message.objects.create(
        user=user,
        chat=chat,
        text=text,
    )


@database_sync_to_async
def add_scheduled_message(
    user: User, chat: Chat, text: str, execute_at: datetime
):
    ScheduledMessage.objects.create(
        user=user, chat=chat, text=text, execute_at=execute_at
    )


@database_sync_to_async
def add_user_to_chat(user: User, chat: Chat):
    if not UserToChat.objects.filter(
        user=user,
        chat=chat,
    ):
        UserToChat.objects.create(
            user=user,
            chat=chat,
        )


@database_sync_to_async
def leave_from_chat(user: User, chat: Chat):
    ...
