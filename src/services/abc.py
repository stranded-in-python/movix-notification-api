from abc import ABC, abstractmethod
from typing import AsyncGenerator, Callable, Iterable
from uuid import UUID

import httpx

from db.notifications import BaseNotificationDatabase
from models.notification_settings import ChannelSettings, NotificationSettings
from models.notifications import GroupedContext, Notification, UserContext
from models.users import UserChannels


class UserServiceABC(ABC):
    client: httpx.AsyncClient

    async def get_users_channels() -> list[UserChannels]:
        ...


class ContextBase(ABC):
    context: Iterable

    def __init__(self, notification: Notification, user_ids: Iterable[UUID]):
        self.notification = notification
        self.user_ids = user_ids

    def hash_context(self, context: UserContext) -> str:
        ...

    async def resolve_context(self) -> Iterable[GroupedContext]:
        """Go to each variable handler"""
        ...


class NotificationServiceABC(ABC):
    notification_db: BaseNotificationDatabase
    get_context_handler: Callable[[Notification, Iterable[UUID]], ContextBase]

    async def get_notification(self, notification_id: UUID) -> Notification | None:
        ...

    async def get_notification_users(
        self, notification_id: UUID
    ) -> AsyncGenerator[list[UUID], None]:
        ...


class NotificationChannelSettingsServiceABC(ABC):
    @abstractmethod
    async def create_channel_setting(
        self, channel: str, enabled: bool, user_id: UUID
    ) -> None | Exception:
        raise NotImplementedError

    @abstractmethod
    async def get_channel_settings(self, user_id: UUID) -> list[ChannelSettings] | None:
        raise NotImplementedError

    @abstractmethod
    async def change_channel_settings(
        self, channel: str, enabled: bool, user_id: UUID
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_channel_settings(self, channel: str, user_id: UUID) -> None:
        raise NotImplementedError


class NotificationSettingsServiceABC(ABC):
    @abstractmethod
    async def create_notification_setting(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ) -> None | Exception:
        raise NotImplementedError

    @abstractmethod
    async def get_notification_settings(
        self, user_id: UUID
    ) -> list[NotificationSettings] | None:
        raise NotImplementedError

    @abstractmethod
    async def change_notification_settings(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_notification_settings(
        self, notification_id: UUID, user_id: UUID
    ) -> None:
        raise NotImplementedError
