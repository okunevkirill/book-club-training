__all__ = [
    "SettingEnvClass",
    "SETTING",
]

import os
from functools import lru_cache
from dotenv import load_dotenv


class SettingEnvClass:
    def __init__(self):
        load_dotenv()

        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_DATABASE_NAME = os.getenv("POSTGRES_DATABASE_NAME")


@lru_cache
def get_setting() -> SettingEnvClass:
    return SettingEnvClass()


SETTING = get_setting()
