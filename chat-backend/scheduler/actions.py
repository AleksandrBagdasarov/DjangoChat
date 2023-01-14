import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from threading import Thread
from time import sleep

import psycopg2.extras
from api.models import User
from chat.settings import DATABASES
from rest_framework_simplejwt.tokens import RefreshToken
from websockets import connect

logger = logging.getLogger("scheduler")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)9s %(asctime)s %(name)s %(message)s: "
)
ch.setFormatter(formatter)
logger.addHandler(ch)


dbname = DATABASES["default"]["NAME"]
user = DATABASES["default"]["USER"]
password = DATABASES["default"]["PASSWORD"]
URL_TO_WS_CHAT = os.getenv("URL_TO_WS_CHAT", "ws://127.0.0.1:8000/ws/chat/")


class ScheduledMessageHandler:
    RUNNING = set()
    CONNECTION = psycopg2.connect(
        f"dbname={dbname} user={user} password={password} host=localhost"
    )
    CURSOR = CONNECTION.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

    @classmethod
    async def _send_to_chat(cls, scheduled_msg):
        # todo split via SOLID
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

        user = User.objects.get(id=user_id)
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        payload = {
            "message": scheduled_msg.text,
            "scheduled_message_id": scheduled_msg.id,
        }
        payload.setdefault("scheduler", True)

        ws_url = f"{URL_TO_WS_CHAT}{chat_id}/?access={access}"
        async with connect(ws_url) as ws:

            payload = json.dumps(payload)
            await ws.send(payload)

    @classmethod
    def _adapter(cls, scheduled_message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(cls._send_to_chat(scheduled_message))
        loop.close()

    @classmethod
    def get_scheduled_messages(cls):
        sql = """
            select * from scheduled_message
            where execute_at < now() + interval '1 minute'
            and executed = false;
            """
        cls.CURSOR.execute(sql)
        scheduled_messages = cls.CURSOR.fetchall()
        for scheduled_msg in scheduled_messages:
            if scheduled_msg.id not in cls.RUNNING:
                cls.RUNNING.add(scheduled_msg.id)
                logger.info(f"Add to Thread JOB.ID {scheduled_msg.id}")
                t = Thread(target=cls._adapter, args=[scheduled_msg])
                t.start()
            else:
                logger.info(f"JOB.ID {scheduled_msg.id} Already in Thread")
