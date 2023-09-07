import os
from uuid import UUID

from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "movix-notifications"

    base_dir = os.path.dirname(os.path.dirname(__file__))


class PublisherProperties(BaseSettings):
    amqp_url: str = (
        "amqp://guest:guest@localhost:5672/"
        "%2F?connection_attempts=3&heartbeat=3600"  # flake8: noqa
    )
    exchange: str = "movix-notification"
    exchange_type: str = "fanout"
    publish_interval: int = 1
    queue: str = "movix-notification"
    routing_key: str = "notification.email"


class EventsProperties(BaseSettings):
    on_registration_id: UUID = ""
    on_registration_vars: list[str] = [""]
    on_registration_send_from: str = "welcom@movix.ru"
    on_registration_subject: str = "Confirm you email"


class UsersProperties(BaseSettings):
    url_get_users_channels: str = "http://localhost:8000/api/v1/notifications/channels"
    url_verify: str = "http://localhost:8000/api/v1/auth/verify"


settings = Settings()
publisher_properties = PublisherProperties()
events_properties = EventsProperties()
user_propertis = UsersProperties()
