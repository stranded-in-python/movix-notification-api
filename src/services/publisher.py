import functools

import aio_pika

from core.config import PublisherProperties, publisher_properties
from core.logger import logger

LOGGER = logger()


class RabbitMQPublisher:
    def __init__(self, properties: PublisherProperties = publisher_properties):
        """Setup the publisher object, passing in the URL we will use
        to connect to RabbitMQ.

        :param str amqp_url: The URL for connecting to RabbitMQ

        """
        self._connection = None
        self._channel = None

        self._deliveries = None
        self._acked = None
        self._nacked = None
        self._message_number = None

        self._stopping = False
        self._url = properties.amqp_url

        self.EXCHANGE = properties.exchange
        self.EXCHANGE_TYPE = properties.exchange_type
        self.PUBLISH_INTERVAL = properties.publish_interval
        self.QUEUE = properties.queue
        self.ROUTING_KEY = properties.routing_key

    async def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection

        """
        LOGGER.info("Connecting to %s", self._url)
        self._connection = await aio_pika.connect_robust(self._url)

    async def open_channel(self):
        """This method will open a new channel with RabbitMQ by issuing the
        Channel.Open RPC command. When RabbitMQ confirms the channel is open
        by sending the Channel.OpenOK RPC reply, the on_channel_open method
        will be invoked.

        """
        LOGGER.info("Creating a new channel")
        self._channel = await self._connection.channel()

    async def publish_message(self, message: str, hdrs: dict | None = None):
        if self._connection is None:
            await self.connect()

        await self.open_channel()

        exchange = await self._channel.get_exchange(
            self.EXCHANGE,
        )
        await exchange.publish(
            aio_pika.Message(bytes(message, encoding="utf8")),
            routing_key=self.ROUTING_KEY,
            timeout=5.0,
        )


@functools.lru_cache
def get_publisher() -> RabbitMQPublisher:
    return RabbitMQPublisher()
