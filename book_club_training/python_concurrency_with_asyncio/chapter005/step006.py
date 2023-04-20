import asyncpg
import asyncio
from base import SETTING


product_query = """
    SELECT
    p.product_id,
    p.product_name,
    p.brand_id,
    s.sku_id,
    pc.product_color_name,
    ps.product_size_name
    FROM product as p
    JOIN sku as s on s.product_id = p.product_id
    JOIN product_color as pc on pc.product_color_id = s.product_color_id
    JOIN product_size as ps on ps.product_size_id = s.product_size_id
    WHERE p.product_id = 100
    """


async def main():
    connection = await asyncpg.connect(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        database=SETTING.POSTGRES_DATABASE_NAME,
        password=SETTING.POSTGRES_PASSWORD,
    )
    print("Creating the product database...")
    queries = [connection.execute(product_query), connection.execute(product_query)]
    results = await asyncio.gather(*queries)
    print(results)


asyncio.run(main())
