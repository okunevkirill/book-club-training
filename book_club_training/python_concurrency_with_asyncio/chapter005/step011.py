import asyncio
import asyncpg
import logging
from base import SETTING


async def main():
    connection = await asyncpg.connect(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        database=SETTING.POSTGRES_DATABASE_NAME,
        password=SETTING.POSTGRES_PASSWORD,
    )
    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")

        try:
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
        except Exception as ex:
            logging.warning("Ошибка при вставке цвета товара игнорируется", exc_info=ex)

        query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'my_new_%'"""
        brands = await connection.fetch(query)
        print(f"Результат запроса: {brands}")
        await connection.close()


asyncio.run(main())
