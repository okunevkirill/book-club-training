import asyncio


async def main() -> None:
    loop = asyncio.get_event_loop()
    loop.slow_callback_duration = 0.250

asyncio.run(main(), debug=True)
