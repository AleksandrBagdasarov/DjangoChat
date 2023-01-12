import asyncio
import json
import logging
from typing import Union

import psycopg2
import psycopg2.extensions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from chat.settings import DATABASES
from websockets import connect

print(DATABASES)

DSN = {
    "database": DATABASES["default"]["NAME"],
    "user": DATABASES["default"]["USER"],
    "password": DATABASES["default"]["PASSWORD"],
}
CONN = psycopg2.connect(DSN)


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        logger = logging.getLogger("sql_debug")
        logger.info(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception as exc:
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise


async def send_to_chat(payload: dict, chat_id: Union[int, str]):
    ws_url = f"ws://127.0.0.1:8000/ws/chat/{chat_id}/"
    async with connect(ws_url) as ws:
        payload.setdefault("scheduled_message", True)
        payload = json.dumps(payload)
        await ws.send(payload)


async def get_jobs():
    # sql = """
    # select * from
    # """
    cur = CONN.cursor(DSN, cursor_factory=LoggingCursor)
    cur.execute()
    jobs = cur.fetch_all()
    print(jobs)


# asyncio.run(send_to_chat())

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_jobs, "interval", seconds=60)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        print("Keyboard interrupt...")
        pass
