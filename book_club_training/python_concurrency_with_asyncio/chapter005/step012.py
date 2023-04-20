import asyncio
import asyncpg
from asyncpg.transaction import Transaction
from base import SETTING


async def main():
    connection = await asyncpg.connect(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        database=SETTING.POSTGRES_DATABASE_NAME,
        password=SETTING.POSTGRES_PASSWORD,
    )
    transaction: Transaction = connection.transaction()
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print("Ошибка, транзакция откатывается!")
        await transaction.rollback()
    else:
        print("Ошибки нет, транзакция фиксируется!")
        await transaction.commit()

    query = "SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'"
    brands = await connection.fetch(query)
    print(brands)

    await connection.close()


asyncio.run(main())
