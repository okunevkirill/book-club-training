import asyncpg
import asyncio
from base import SETTING


async def take(generator, to_take: int):
    item_count = 0
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count += 1
        yield item


async def main():
    connection = await asyncpg.connect(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        database=SETTING.POSTGRES_DATABASE_NAME,
        password=SETTING.POSTGRES_PASSWORD,
    )
    async with connection.transaction():
        query = "SELECT product_id, product_name from product"
        product_generator = connection.cursor(query)

        async for product in take(product_generator, 5):
            print(product)

        print("Получены первые пять товаров!")

    await connection.close()


asyncio.run(main())
