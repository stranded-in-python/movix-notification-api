import functools
from uuid import UUID

import httpx
import orjson

from core.config import user_propertis
from models.users import UserSettings
from services.abc import UserServiceABC


class UserService(UserServiceABC):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_user_settings(self, user_ids: list[UUID]) -> UserSettings:
        user_settings = await self._get_user_settings(user_ids)

        for index, settings in enumerate(user_settings):
            user_settings[index] = UserSettings(
                id=settings.id, type=settings.type, value=settings.value
            )

        return user_settings

    async def _get_user_settings(self, user_ids: list[UUID]):
        url = user_propertis.url_get_users_settings
        response = await self.client.post(url, json=orjson.dumps(user_ids))
        if response.status_code == 200:
            return response.json()

        response.raise_for_status()


@functools.lru_cache
def get_user_service() -> UserService:
    return UserService(httpx.AsyncClient())
