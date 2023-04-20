import asyncio
import logging
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
    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            await connection.execute(insert_brand)
    except Exception:
        logging.exception("Ошибка при выполнении транзакции")
    finally:
        query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'big_%'"""
        brands = await connection.fetch(query)
        print(f"Результат запроса: {brands}")

        await connection.close()


asyncio.run(main())
