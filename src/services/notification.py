from functools import lru_cache

# from core.config import settings
from models.notifications import Notification, NotificationRecipient

from .abc import NotificationServiceABC


class NotificationService(NotificationServiceABC):
    def send_message():
        ...

    def get_notification(nitification_id) -> Notification:
        ...

    def get_notification_users(nitification_id, offset) -> list[NotificationRecipient]:
        # limit = settings.users_limit
        ...


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService()
