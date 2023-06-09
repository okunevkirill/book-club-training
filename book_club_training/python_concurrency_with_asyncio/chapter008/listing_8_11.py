import asyncio
import asyncpg
import os
import tty
from base import SETTING
from collections import deque
from asyncpg.pool import Pool
from listing_8_5 import create_stdin_reader
from listing_8_7 import *
from listing_8_8 import read_line
from listing_8_9 import MessageStore


async def run_query(query: str, pool: Pool, message_store: MessageStore):
    async with pool.acquire() as connection:
        try:
            result = await connection.fetchrow(query)
            await message_store.append(
                f"Выбрано {len(result)} строк по запросу: {query}"
            )
        except Exception as err:
            await message_store.append(f"Получено исключение {err} от: {query}")


async def main():
    tty.setcbreak(0)
    os.system("clear")
    rows = move_to_bottom_of_screen()

    async def redraw_output(items: deque):
        save_cursor_position()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            print(item)
        restore_cursor_position()

    messages = MessageStore(redraw_output, rows - 1)

    stdin_reader = await create_stdin_reader()

    async with asyncpg.create_pool(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        password=SETTING.POSTGRES_PASSWORD,
        database=SETTING.POSTGRES_DATABASE_NAME,
        min_size=6,
        max_size=6,
    ) as pool:
        while True:
            query = await read_line(stdin_reader)
            asyncio.create_task(run_query(query, pool, messages))


asyncio.run(main())
