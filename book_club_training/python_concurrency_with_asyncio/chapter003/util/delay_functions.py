import asyncio
from time import perf_counter
from functools import wraps


def async_timer(func):
    @wraps(func)
    async def wrapped(*args, **kwargs):
        start = perf_counter()
        result = await func(*args, **kwargs)
        print(f"{func} завершилась за {perf_counter() - start} с")
        return result

    return wrapped


async def delay(delay_seconds: int) -> int:
    print(f"засыпаю на {delay_seconds} с")
    await asyncio.sleep(delay_seconds)
    print(f"сон в течении {delay_seconds} с закончился")
    return delay_seconds
