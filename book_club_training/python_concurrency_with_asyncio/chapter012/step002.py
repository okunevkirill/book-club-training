import asyncio
from asyncio import Queue


async def main():
    customer_queue = Queue()
    customer_queue.get_nowait()


asyncio.run(main())
