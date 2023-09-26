import os
from logging import config as logging_config
from uuid import UUID

from pydantic import BaseSettings

from core.logger import LOG_LEVEL, get_logging_config


class Settings(BaseSettings):
    project_name: str = "movix-notifications"

    base_dir = os.path.dirname(os.path.dirname(__file__))

    # Настройки PSQL
    pghost: str = "localhost"
    pgport: str = "5434"
    pgdb: str = "yamp_movies_db"
    pguser: str = "yamp_dummy"
    pgpassword: str = "qweasd123"
    database_adapter: str = "postgresql"
    database_sqlalchemy_adapter: str = "postgresql+asyncpg"

    log_level: str = LOG_LEVEL

    pack_size: int = 1000

    sentry_dsn_api: str = ""

class PublisherProperties(BaseSettings):
    amqp_url: str = (
        "amqp://guest:guest@localhost:5672/"
        "%2F?connection_attempts=3&heartbeat=60"  # flake8: noqa
    )
    exchange: str = "movix-notification"
    exchange_type: str = "fanout"
    publish_interval: int = 1
    queue: str = "movix-notification"
    routing_key: str = "notification.email"


class EventsProperties(BaseSettings):
    on_registration_template_id: UUID = UUID(int=0)
    on_registration_vars: list[str] = [""]
    on_registration_send_from: str = "welcome@movix.ru"
    on_registration_subject: str = "Confirm you email"


class UsersProperties(BaseSettings):
    url_get_users_channels: str = "http://auth:8000/api/v1/users/channels"
    url_get_users: str = "http://auth:8000/api/v1/users"
    url_verify: str = "http://auth:8000/api/v1/auth/verify"
    users_limit: int = 60000
    access_token: str = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZT"
        "RlZmEzNy0xMTkxLTQ3NzEtODExYy00MjgxOGIzYjJjYTkiLCJhdWQiOlsibW92aXg6"
        "YXV0aCJdLCJleHAiOjE2OTQ1NTkwMzh9.wd0HC8lvWWofEOv94EeNiM9QDd95zh-8O"
        "QjUxs8nfIs"
    )
    username: str = "AlanX9"
    password: str = "123qwe"
    url_refresh_token: str = "http://auth:8000/api/v1/refresh"
    url_login: str = "http://auth:8000/api/v1/login"
    notifications_email_from: str = "notifications@movix.ru"


settings = Settings()

if settings.sentry_dsn_api:
    import sentry_sdk  # type: ignore

    sentry_sdk.init(dsn=settings.sentry_dsn_api, traces_sample_rate=1.0)

publisher_properties = PublisherProperties()
events_properties = EventsProperties()
user_properties = UsersProperties()
authorization_data = {"access_token": "", "refresh_token": ""}


def get_database_url_async() -> str:
    return (
        f"{settings.database_sqlalchemy_adapter}://{settings.pguser}:"
        f"{settings.pgpassword}@{settings.pghost}:{settings.pgport}/{settings.pgdb}"
    )


logging_config.dictConfig(get_logging_config(level=settings.log_level))
