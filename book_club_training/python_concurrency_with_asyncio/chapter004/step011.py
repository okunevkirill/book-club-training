import asyncio
import aiohttp
from util import async_timed
from chapter_04 import fetch_status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, "https://www.google.ru/", 1),
            fetch_status(session, "https://www.google.ru/", 10),
            fetch_status(session, "https://www.google.ru/", 10),
        ]

        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print("Произошёл тайм-аут!")

        for task in asyncio.all_tasks():
            print(task)


asyncio.run(main())
