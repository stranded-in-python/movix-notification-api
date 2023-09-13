from typing import AsyncGenerator, Callable, Iterable
from uuid import UUID

from fastapi import Depends

from core.config import user_propertis
from db.notifications import SANotificationDB, get_notification_db
from models.notifications import Notification
from services.context import Context, get_context_handler_dependency

from .abc import NotificationServiceABC


class NotificationService(NotificationServiceABC):
    notification_db: SANotificationDB
    get_context_handler: Callable[[Notification, Iterable[UUID]], Context]

    def __init__(
        self,
        notification_db: SANotificationDB,
        get_context_handler: Callable[[Notification, Iterable[UUID]], Context],
    ):
        self.notification_db = notification_db
        self.get_context_handler = get_context_handler

    async def get_notification(self, notification_id: UUID) -> Notification | None:
        return await self.notification_db.get_notification(notification_id)

    async def get_notification_users(
        self, notification_id: UUID
    ) -> AsyncGenerator[list[UUID], None]:
        async for users_ids in self.notification_db.get_notification_users(
            notification_id=notification_id, users_limit=user_propertis.users_limit
        ):
            yield users_ids

    async def generate_context(
        self, notification: Notification, user_ids: Iterable[UUID]
    ) -> list:
        handler = self.get_context_handler(notification, user_ids)
        handler.resolve_context()
        return handler.context


async def get_notification_service(
    get_context_handler: Callable[[Notification, Iterable[UUID]], Context] = Depends(
        get_context_handler_dependency
    ),
    notification_db: SANotificationDB = Depends(get_notification_db),
) -> AsyncGenerator[NotificationService, None]:
    yield NotificationService(notification_db, get_context_handler)
