import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from typing import List, Dict
from base import SETTING


async def create_database_pool():
    pool: Pool = await asyncpg.create_pool(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        password=SETTING.POSTGRES_PASSWORD,
        database=SETTING.POSTGRES_DATABASE_NAME,
        min_size=6,
        max_size=6,
    )
    app.state.DB = pool


async def destroy_database_pool():
    pool = app.state.DB
    await pool.close()


async def brands(request: Request) -> Response:
    connection: Pool = request.app.state.DB
    brand_query = "SELECT brand_id, brand_name FROM brand"
    results: List[Record] = await connection.fetch(brand_query)
    result_as_dict: List[Dict] = [dict(brand) for brand in results]
    return JSONResponse(result_as_dict)


app = Starlette(
    routes=[Route("/brands", brands)],
    on_startup=[create_database_pool],
    on_shutdown=[destroy_database_pool],
)
