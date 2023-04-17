import asyncio
import aiohttp
from chapter_04 import fetch_status
from util import async_timed


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.google.ru/"
        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]
        while pending:
            done, pending = await asyncio.wait(
                pending, return_when=asyncio.FIRST_COMPLETED
            )

            print(f"Число завершившихся задач: {len(done)}")
            print(f"Число ожидающих задач: {len(pending)}")

            for done_task in done:
                print(await done_task)


asyncio.run(main())
