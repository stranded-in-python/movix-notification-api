import os
from pika import AMQPConnectionWorkflow

from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "movix-notifications"

    base_dir = os.path.dirname(os.path.dirname(__file__))
    # rebbitmq_amqp_url: str = "amqp://guest:guest@localhost:5672/%2F?connection_attempts=3&heartbeat=3600"
    # connection_errors = (
    #     AMQPConnectionWorkflow,
    # )

class PublisherProperties(BaseSettings):
    amqp_url: str = "amqp://guest:guest@localhost:5672/%2F?connection_attempts=3&heartbeat=3600"
    exchange: str = 'movix-notification'
    exchange_type: str = "fanout"
    publish_interval: int = 1
    queue: str = 'movix-notification'
    routing_key: str = 'notification.email'


settings = Settings()
publisher_properties = PublisherProperties()

