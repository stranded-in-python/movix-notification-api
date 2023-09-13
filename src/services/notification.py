from typing import AsyncGenerator
from uuid import UUID

from fastapi import Depends

from core.config import user_propertis
from db.notifications import SANotificationDB, get_notification_db
from models.notifications import Notification

from .abc import NotificationServiceABC


class NotificationService(NotificationServiceABC):
    notification_db: SANotificationDB

    def __init__(self, notification_db: SANotificationDB):
        self.notification_db = notification_db

    async def get_notification(self, notification_id: UUID) -> Notification | None:
        return await self.notification_db.get_notification(notification_id)

    async def get_notification_users(
        self, notification_id: UUID
    ) -> AsyncGenerator[list[UUID], None]:
        async for users_ids in self.notification_db.get_notification_users(
            notification_id=notification_id, users_limit=user_propertis.users_limit
        ):
            yield users_ids


async def get_notification_service(
    notification_db: SANotificationDB = Depends(get_notification_db),
) -> AsyncGenerator[NotificationService, None]:
    yield NotificationService(notification_db)
