from typing import AsyncGenerator
from uuid import UUID

from core.config import user_propertis
from db.notifications import SANotificationDB
from models.notifications import Notification
from services.user import UserService

from .abc import NotificationServiceABC


class NotificationService(NotificationServiceABC):
    notification_db: SANotificationDB
    user_service: UserService

    async def get_notification(self, notification_id) -> Notification | None:
        return await self.notification_db.get_notification(notification_id)

    async def get_notification_users(
        self, notification_id, offset
    ) -> AsyncGenerator[list[UUID], None]:
        async for users_ids in self.notification_db.get_notification_users_generator(
            notification_id=notification_id,
            users_limit=user_propertis.users_limit,
        ):
            yield users_ids


def get_notification_service() -> NotificationService:
    return NotificationService()
