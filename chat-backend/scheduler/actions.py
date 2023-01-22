import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from threading import Thread
from time import sleep

import psycopg2.extras
from api.models import User
from asgiref.sync import sync_to_async
from chat.settings import DATABASES
from rest_framework_simplejwt.tokens import RefreshToken
from websocket.serializers import ReceiveJsonTypes
from websockets import connect

logger = logging.getLogger("scheduler")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)9s %(asctime)s %(name)s: %(message)s "
)
ch.setFormatter(formatter)
logger.addHandler(ch)


dbname = DATABASES["default"]["NAME"]
dbuser = DATABASES["default"]["USER"]
password = DATABASES["default"]["PASSWORD"]
URL_TO_WS_CHAT = os.getenv("URL_TO_WS_CHAT", "ws://127.0.0.1:8000/ws/chat/")


@sync_to_async
def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        logger.error(e)


class ScheduledMessageHandler:
    RUNNING = set()
    CONNECTION = psycopg2.connect(
        f"dbname={dbname} user={dbuser} password={password} host=localhost"
    )
    CURSOR = CONNECTION.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    @classmethod
    async def _send_to_chat(cls, scheduled_msg):
        logger.info(f"In Thread running {scheduled_msg.id}")
        now = datetime.now(tz=timezone.utc)
        now_time_start = now.strftime("%H:%M:%S")
        scheduled_msg.execute_at.replace(tzinfo=timezone.utc)
        execute_at_time = scheduled_msg.execute_at.strftime("%H:%M:%S")
        execute_in = (scheduled_msg.execute_at - now).total_seconds()

        if execute_in > 0:
            sleep(int(execute_in))

        now = datetime.now(tz=timezone.utc)
        now_time_end = now.strftime("%H:%M:%S")
        logger.info(f"start       : {now_time_start}")
        logger.info(f"end         : {now_time_end}")
        logger.info(f"execute_at  : {execute_at_time}")
        logger.info(f"execute_in  : {execute_in}")
        logger.info("")
        logger.info("#" * 20)

        chat_id = scheduled_msg.chat_id
        user_id = scheduled_msg.user_id
        ws_url = f"{URL_TO_WS_CHAT}{chat_id}/"
        if user_id:
            user = await get_user(user_id)
            if user:
                refresh = RefreshToken.for_user(user)
                access = str(refresh.access_token)
                ws_url += f"?access={access}"

        payload = {
            "type": ReceiveJsonTypes.SCHEDULER,
            "message": scheduled_msg.text,
            "scheduled_message_id": scheduled_msg.id,
        }
        payload.setdefault("scheduler", True)

        async with connect(ws_url) as ws:

            payload = json.dumps(payload)
            await ws.send(payload)

    @classmethod
    def _adapter(cls, scheduled_message):
        """Create async loop in thread and call ws client"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(cls._send_to_chat(scheduled_message))
        loop.close()

    @classmethod
    def _get_scheduled_messages(cls):
        sql = """
            select * from scheduled_message
            where execute_at < now() + interval '1 minute'
            and executed = false;
            """
        cls.CURSOR.execute(sql)
        scheduled_messages = cls.CURSOR.fetchall()
        return scheduled_messages

    @classmethod
    def _crate_ws_client_threads(cls, scheduled_messages: list):
        for scheduled_msg in scheduled_messages:
            if scheduled_msg.id not in cls.RUNNING:
                cls.RUNNING.add(scheduled_msg.id)
                logger.info(f"Add to Thread JOB.ID {scheduled_msg.id}")
                t = Thread(target=cls._adapter, args=[scheduled_msg])
                t.start()
            else:
                logger.info(f"JOB.ID {scheduled_msg.id} Already in Thread")

    @classmethod
    def start(cls):
        scheduled_messages = cls._get_scheduled_messages()
        cls._crate_ws_client_threads(scheduled_messages)


def start():
    logger.info("info")
    smh = ScheduledMessageHandler()
    smh.start()
