import asyncpg
import asyncio
from base import SETTING


async def main():
    connection = await asyncpg.connect(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        database=SETTING.POSTGRES_DATABASE_NAME,
        password=SETTING.POSTGRES_PASSWORD,
    )
    version = connection.get_server_version()
    print(f"Подключено! Версия Postgres равна {version}")
    await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
