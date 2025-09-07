from os import getenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = getenv('ENV')
    DATABASE_URL: str = getenv('DATABASE_URL')
    JWT_SECRET: str = getenv('JWT_SECRET')
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60


settings = Settings()
