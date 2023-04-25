import functools
import requests
import asyncio
from util import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    loop = asyncio.get_running_loop()
    urls = ["https://www.example.com" for _ in range(100)]
    tasks = [
        loop.run_in_executor(None, functools.partial(get_status_code, _url))
        for _url in urls
    ]
    result = await asyncio.gather(*tasks)
    print(result)


asyncio.run(main())
