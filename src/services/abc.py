from abc import ABC
from typing import AsyncGenerator, Callable, Iterable
from uuid import UUID

import httpx

from db.notifications import BaseNotificationDatabase
from models.notifications import Notification
from models.users import UserChannels
from services.context import Context


class UserServiceABC(ABC):
    client: httpx.AsyncClient

    async def get_users_channels() -> list[UserChannels]:
        ...


class NotificationServiceABC(ABC):
    notification_db: BaseNotificationDatabase
    get_context_handler: Callable[[Notification, Iterable[UUID]], Context]

    async def get_notification(self, notification_id: UUID) -> Notification | None:
        ...

    async def get_notification_users(
        self, notification_id: UUID
    ) -> AsyncGenerator[list[UUID], None]:
        ...
