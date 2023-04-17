import asyncio
import aiohttp


async def fetch_status(session: aiohttp.ClientSession, url: str) -> int:
    ten_mills = aiohttp.ClientTimeout(total=0.01)
    async with session.get(url, timeout=ten_mills) as result:
        return result.status


async def main():
    session_timeout = aiohttp.ClientTimeout(total=1, connect=0.1)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        await fetch_status(session, "https://www.google.ru/")


asyncio.run(main())
