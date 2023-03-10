from pydantic import BaseSettings, Field


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

    limiter_config: str = Field('10 per 1 minute', env='LIMITER_CONFIG')
    

class JaegerSettings(Settings):
    agent_host: str = Field('jaeger', env='JAEGER_HOST')
    agent_port: int = Field(6831, env='JAEGER_AGENT_PORT')
    sampling_ratio: float = Field(0.8, env='JAEGER_SAMPLING_RATIO')
    auth_project_name: str = Field('AuthorizationService', env='AUTH_PROJECT_NAME')
    

class OauthClientSettings(Settings):
    google_client_id: str = Field('', env='GOOGLE_CLIENT_ID')
    google_client_secret: str = Field('', env='GOOGLE_CLIENT_SECRET')
    google_server_metadata_url: str = Field(
        'https://accounts.google.com/.well-known/openid-configuration',
        env='GOOGLE_SERVER_METADATA_URL'
    )

    yandex_client_id: str = Field('', env='YANDEX_CLIENT_ID')
    yandex_client_secret: str = Field('', env='YANDEX_CLIENT_SECRET')
    yandex_access_token_url: str = Field('https://oauth.yandex.ru/token', env='YANDEX_ACCESS_TOKEN_URL')
    yandex_authorize_url: str = Field('https://oauth.yandex.ru/authorize', env='YANDEX_AUTHORIZE_URL')
    yandex_api_base_url: str = Field('https://login.yandex.ru/info', env='YANDEX_API_BASE_URL')

settings = Settings()
oauth_settings = OauthClientSettings()
jaeger_settings = JaegerSettings()

GOOGLE_CLIENT_ID = oauth_settings.google_client_id
GOOGLE_CLIENT_SECRET = oauth_settings.google_client_secret

YANDEX_CLIENT_ID = oauth_settings.yandex_client_id
YANDEX_CLIENT_SECRET = oauth_settings.yandex_client_secret
