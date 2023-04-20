import asyncpg
import asyncio
import asyncpg
from base import SETTING


async def main():
    connection = await asyncpg.connect(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        database=SETTING.POSTGRES_DATABASE_NAME,
        password=SETTING.POSTGRES_PASSWORD,
    )
    query = "SELECT product_id, product_name FROM product"
    async with connection.transaction():
        async for product in connection.cursor(query):
            print(product)

    await connection.close()


asyncio.run(main())
