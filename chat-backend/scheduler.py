import asyncio
import json
import logging
from datetime import datetime, timezone, tzinfo
from threading import Thread
from time import sleep
from typing import Union

import psycopg2
import psycopg2.extensions
import psycopg2.extras
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from chat.settings import DATABASES
from websockets import connect

DSN = {
    "dbname": DATABASES["default"]["NAME"],
    "user": DATABASES["default"]["USER"],
    "password": DATABASES["default"]["PASSWORD"],
}
dbname = DSN["dbname"]
user = DSN["user"]
password = DSN["password"]

print(DSN)


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


async def test_(job):
    print(f"start       : {job.id}")
    now = datetime.now(tz=timezone.utc)
    now_time_start = now.strftime("%H:%M:%S")

    job.execute_at.replace(tzinfo=timezone.utc)
    execute_at_time = job.execute_at.strftime("%H:%M:%S")
    execute_in = (job.execute_at - now).total_seconds()
    if execute_in > 0:
        sleep(int(execute_in))
    now = datetime.now(tz=timezone.utc)
    now_time_end = now.strftime("%H:%M:%S")
    print(f"start       : {now_time_start}")
    print(f"end         : {now_time_end}")
    print(f"execute_at  : {execute_at_time}")
    print(f"execute_in  : {execute_in}")
    print()
    print("#" * 20)


def adapter(job):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_(job))
    loop.close()


async def get_jobs():
    sql = """
    select * from scheduled_message
    where execute_at < now() + interval '1 minute'
    and executed = false
    """
    CONN = psycopg2.connect(
        f"dbname={dbname} user={user} password={password} host=localhost"
    )
    cur = CONN.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute(
        sql,
    )
    jobs = cur.fetchall()
    tasks = set()
    for job in jobs:
        t = Thread(target=adapter, args=[job])
        t.start()
        # task = asyncio.create_task(test_(job))
        # tasks.add(task)
        # now = datetime.now(tz=timezone.utc)
    # await asyncio.gather(*tasks)
    # print("execute_at:", job.execute_at.strftime('%H:%M:%S'))
    # print("now       :", now.strftime('%H:%M:%S'))
    # print("execute in:", (job.execute_at - now).total_seconds())
    # print("#" * 10)
    print("jobs", jobs)
    print(". " * 10)


if __name__ == "__main__":
    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(get_jobs, "interval", seconds=60)
    # scheduler.start()
    # try:
    #     asyncio.get_event_loop().run_forever()
    # except (KeyboardInterrupt, SystemExit):
    #     print("Keyboard interrupt...")
    #     pass
    asyncio.run(get_jobs())
