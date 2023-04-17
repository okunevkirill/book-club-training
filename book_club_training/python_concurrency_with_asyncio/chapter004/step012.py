import asyncio
import aiohttp
from util import async_timed
from chapter_04 import fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "https://www.google.ru/"),
            fetch_status(session, "https://www.google.ru/"),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f"Число завершившихся задач: {len(done)}")
        print(f"Число ожидающих задач: {len(pending)}")

        for done_task in done:
            result = await done_task
            print(result)


asyncio.run(main())
