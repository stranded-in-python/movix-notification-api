import uuid
from uuid import UUID

import httpx
import orjson

from core.config import authorization_data, user_propertis
from core.logger import logger
from models.users import NotificationChannel, UserChannels
from services.abc import UserServiceABC

LOGGER = logger()


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
        access_token = await self._get_access_token()
        print(access_token)
        headers = {
            'Content-Type': "application/json",
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': f'Bearer {access_token}',
        }
        request = httpx.Request(
            'GET', url, content=orjson.dumps(user_ids), headers=headers
        )
        response = await self.client.send(request=request)
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

    async def _get_access_token(self) -> str | None:
        refresh_token = await self._get_refresh_token()

        url = user_propertis.url_refresh_token
        headers = {
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': f'Bearer {refresh_token}',
        }
        request = httpx.Request('POST', url, headers=headers)
        response = await self.client.send(request=request)
        LOGGER.info(response.status_code)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            await self._set_access_token(access_token)
            return access_token
        response.raise_for_status()

    async def _get_refresh_token(self) -> str | None:

        url = user_propertis.url_login
        headers = {
            # 'Content-Type': "multipart/form-data",
            'X-Request-Id': str(uuid.uuid4())
        }
        data = {
            "username": user_propertis.username,
            "password": user_propertis.password,
        }
        response = await self.client.post(url=url, headers=headers, data=data)
        if response.status_code == 200:
            refresh_token = response.json()['refresh_token']
            await self._set_refresh_token(refresh_token)
            return refresh_token
        response.raise_for_status()

    async def _set_access_token(self, access_token):
        authorization_data['access_token'] = access_token

    async def _set_refresh_token(self, refresh_token):
        authorization_data['refresh_token'] = refresh_token


async def get_user_service() -> UserService:
    yield UserService(httpx.AsyncClient())
