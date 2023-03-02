import os

from dotenv import load_dotenv
from pydantic import BaseSettings

IS_DOCKER = os.environ.get('DOCKER_CONTAINER', False)

if not IS_DOCKER:
    load_dotenv()


class Settings(BaseSettings):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SERVICE_URL: str = os.getenv("APP_URL")
    
    USERNAME = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('PG_HOST')
    PORT = os.getenv('PG_PORT')
    DATABASE_NAME = os.getenv('POSTGRES_DB')

    REDIS_PORT: str = os.getenv('REDIS_PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PromSettings(Settings):

    REDIS_HOST: str = os.getenv('REDIS_HOST')


class DevSettings(Settings):

    REDIS_HOST: str

    class Config:
        fields = {
            "REDIS_HOST": {
                'env': 'REDIS_HOST_DEBUG'
            }
        }


def get_settings():
    environment = os.getenv('ENVIRONMENT')
    if environment == 'prom':
        return get_prom_settings()
    else:
        return get_dev_settings()


def get_prom_settings():
    return PromSettings()


def get_dev_settings():
    return DevSettings()
