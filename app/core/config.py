from functools import lru_cache
from pydantic_settings import BaseSettings,SettingConfigDict
from sqlalchemy import URL

class Settings(BaseSettings):
    DB_HOST:str
    DB_PORT:int
    DB_NAME:str
    DB_USER:str
    DB_PASSWORD:str

    model_config = SettingConfigDict(
        env_file = ".env",
        extra = "ignore"
    )

    @property
    def database_url(self)->URL:
        return URL.create(
            "postgresql+asyncpg",
            username = self.DB_USER,
            password = self.DB_PASSWORD,
            host = self.DB_HOST,
            port = self.DB_PORT,
            database=self.DB_NAME
        )


@lru_cache
def get_settings():
    return Settings()
