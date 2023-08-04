import functools
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from listing_10_4 import DB_KEY, create_database_pool, destroy_database_pool
from base import SETTING


routes = web.RouteTableDef()


@routes.get("/products")
async def products(request: Request) -> Response:
    db = request.app[DB_KEY]
    product_query = "SELECT product_id, product_name FROM product"
    result = await db.fetch(product_query)
    return web.json_response([dict(record) for record in result])


app = web.Application()
app.on_startup.append(
    functools.partial(
        create_database_pool,
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        password=SETTING.POSTGRES_PASSWORD,
        database="products",
    )
)
app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)
web.run_app(app, port=8000)