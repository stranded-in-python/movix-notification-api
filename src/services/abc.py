from abc import ABC

from db.notifications import BaseNotificationDatabase
from models.users import UserChannels


class QueueABC(ABC):
    def push(self, element):
        ...


class UserServiceABC(ABC, UserChannels):
    async def get_users_channels() -> list[UserChannels]:
        ...


class NotificationServiceABC(ABC):
    queue: QueueABC
    notification_db: BaseNotificationDatabase
    user_service: UserServiceABC

    def send_message():
        ...
