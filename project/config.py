from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # pydantic settings reads from env variables and .env file

    DATABASE_URL: str
    APP_NAME: str = 'AI BACKEND API'
    DEBUG: bool = False
    REDIS_URL: str

    model_config = SettingsConfigDict(env_file='.env')


@lru_cache()
def get_settings():
    return Settings() # type: ignore

