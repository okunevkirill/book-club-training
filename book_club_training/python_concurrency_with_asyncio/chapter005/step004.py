import asyncpg
import asyncio
from pathlib import Path
from typing import Tuple, Union, List
from random import sample
from base import SETTING


def load_common_words() -> List[str]:
    with Path("common_words.txt").open() as common_words:
        return [word.strip() for word in common_words.readlines()]


def generate_brand_names(words: List[str]) -> List[Tuple[Union[str]]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    _insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(_insert_brands, brands)


async def main():
    common_words = load_common_words()
    connection = await asyncpg.connect(
        host=SETTING.POSTGRES_HOST,
        port=SETTING.POSTGRES_PORT,
        user=SETTING.POSTGRES_USER,
        database=SETTING.POSTGRES_DATABASE_NAME,
        password=SETTING.POSTGRES_PASSWORD,
    )
    await insert_brands(common_words, connection)


asyncio.run(main())
