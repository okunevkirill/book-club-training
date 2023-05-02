import functools
import time
from typing import Callable, Any


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"выполняется {func} с аргументами {args} {kwargs}")
            start = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.perf_counter()
                total = end - start
                print(f"{func} завершилась за {total:.4f} с")

        return wrapped

    return wrapper


def my_async_timer(func):
    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        print(f"выполняется {func} с аргументами {args} {kwargs}")
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        print(f"{func} завершилась за {time.perf_counter() - start:.4f} с")
        return result

    return wrapped
