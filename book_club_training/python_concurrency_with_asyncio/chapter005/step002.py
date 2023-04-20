import asyncio
import asyncpg
import scripts as sq
from base import SETTING


async def main():
    connection = await asyncpg.connect(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        database=SETTING.POSTGRES_DATABASE_NAME,
        password=SETTING.POSTGRES_PASSWORD,
    )
    statements = [
        sq.CREATE_BRAND_TABLE,
        sq.CREATE_PRODUCT_TABLE,
        sq.CREATE_PRODUCT_COLOR_TABLE,
        sq.CREATE_PRODUCT_SIZE_TABLE,
        sq.CREATE_SKU_TABLE,
        sq.SIZE_INSERT,
        sq.COLOR_INSERT,
    ]

    print("Создается база данных product...")
    for statement in statements:
        status = await connection.execute(statement)
        print(status)
    print("База данных product создана!")
    await connection.close()


asyncio.run(main())
