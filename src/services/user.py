from uuid import UUID

import httpx
import orjson

from core.config import user_propertis
from core.logger import logger
from models.users import NotificationChannel, UserChannels
from services.abc import UserServiceABC


class UserService(UserServiceABC):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_users_channels(self, user_ids: list[UUID]) -> list[UserChannels]:
        users_channels = await self._get_users_channels(user_ids)

        serialized_channels = await self._serialize_users_channels(users_channels)

        return serialized_channels

    async def _get_users_channels(self, user_ids: list[UUID]) -> list[dict]:
        """
        Retrieves the channels associated with the specified user IDs.

        Args:
            user_ids (list[UUID]): A list of UUIDs representing the user IDs.

        Returns:
            dict: A dictionary containing the response JSON if the request is successful.

        Raises:
            HTTPError: If the request fails with a non-200 status code.
        """
        url = user_propertis.url_get_users_channels
        response = await self.client.post(url, data=orjson.dumps(user_ids))
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()

    async def _serialize_users_channels(
        self, _users_channels: list[dict]
    ) -> list[UserChannels]:
        """
        Serializes a list of users channels.

        Args:
            _users_channels (list[dict]): A list of dictionaries representing user channels.

        Returns:
            UserChannels: The serialized user channels.

        Raises:
            Exception: If there is an error during serialization.
        """
        users_channels = []

        for _user_channels in _users_channels:
            try:
                channels = [
                    NotificationChannel(type=channel["type"], value=channel["value"])
                    for channel in _user_channels["channels"]
                ]

                user_channels = UserChannels(id=_user_channels["id"], channels=channels)
                users_channels.append(user_channels)
            except Exception as e:
                logger.error(f"Invalid user channels: {channels}. {e}")

        return users_channels


def get_user_service() -> UserService:
    return UserService(httpx.AsyncClient())
