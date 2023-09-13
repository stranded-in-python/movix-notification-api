from abc import ABC
from typing import AsyncGenerator, Callable, Iterable
from uuid import UUID

import httpx

from db.notifications import BaseNotificationDatabase
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
