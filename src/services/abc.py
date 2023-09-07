from abc import ABC

from models.users import UserSettings


class QueueABC(ABC):
    def push(self, element):
        ...


class NotificationServiceABC(ABC):
    queue: QueueABC

    def send_message():
        ...


class UserServiceABC(ABC, UserSettings):
    async def get_users_settings() -> list[UserSettings]:
        ...
