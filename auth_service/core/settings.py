
from pathlib import Path

from logging import config as logging_config
from pydantic import BaseSettings, Field

from core.logger import LOGGING


class Settings(BaseSettings):
    app_url: str = Field('http://localhost', env='APP_URL')

    pg_host: str = Field('127.0.0.1', env='PG_HOST')
    pg_port: int = Field(5433, env='PG_PORT')
    postgres_user: str = Field('app', env='POSTGRES_USER')
    postgres_password: str = Field('123qwe', env='POSTGRES_PASSWORD')
    postgres_db: str = Field('auth_database', env='POSTGRES_DB')

    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    redis_db_int: int = Field(0, env='REDIS_DB_INT')
    redis_password: str = Field('', env='REDIS_PASSWORD')
    compose_hostname: str = Field('redis', env='COMPOSE_HOSTNAME')

    admin_username: str = Field('admin', env='ADMIN_USERNAME')
    admin_password: str = Field('admin', env='ADMIN_PASSWORD')

    jwt_secret_key: str = Field('qTFToYm{b6XuYnQPYG|H6GY|5eIR6|sv', env='JWT_SECRET_KEY')
    jwt_access_token_expires: int = Field(120, env='JWT_ACCESS_TOKEN_EXPIRES')
    jwt_refresh_token_expires: int = Field(120, env='JWT_REFRESH_TOKEN_EXPIRES')

settings = Settings()
