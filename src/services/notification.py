from functools import lru_cache

from .abc import NotificationServiceABC


class NotificationService(NotificationServiceABC):
    def send_message():
        ...


@lru_cache
def get_notification_service() -> NotificationService:
    return NotificationService()
