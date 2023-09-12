from abc import ABC, abstractmethod
from typing import AsyncGenerator
from uuid import UUID

import httpx

from db.notifications import BaseNotificationDatabase
from models.notifications import Notification
from models.users import UserChannels


class UserServiceABC(ABC):
    client: httpx.AsyncClient

    async def get_users_channels() -> list[UserChannels]:
        ...


class NotificationServiceABC(ABC):
    notification_db: BaseNotificationDatabase

    async def get_notification(self, notification_id: UUID) -> Notification | None:
        ...

    async def get_notification_users(
        self, notification_id: UUID
    ) -> AsyncGenerator[list[UUID], None]:
        ...

class NotificationChannelSettingsServiceABC(ABC):
    @abstractmethod
    async def create_channel_setting(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_channel_settings(self, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def change_channel_settings(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def delete_channel_settings(self, channel: str, user_id: UUID):
        raise NotImplementedError


class NotificationSettingsServiceABC(ABC):
    @abstractmethod
    async def create_notification_setting(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        raise NotImplementedError

    @abstractmethod
    async def get_notification_settings(self, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def change_notification_settings(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete_notification_settings(self, notification_id: UUID, user_id: UUID):
        raise NotImplementedError
