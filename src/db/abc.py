from abc import ABC, abstractmethod
from uuid import UUID

class NotificationSettingsChannelDBABC(ABC):
    @abstractmethod
    async def create(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: UUID, channel: str):
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, user_id: UUID):
        raise NotImplementedError
    
    @abstractmethod
    async def change(self, channel: str, enabled: bool, user_id: UUID):
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, channel: str, user_id: UUID):
        raise NotImplementedError


class NotificationSettingsDBABC(ABC):
    @abstractmethod
    async def create(self, notification_id: UUID, disabled: bool, user_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get(self, user_id: UUID, notification_id: UUID):
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, user_id: UUID):
        raise NotImplementedError
    
    @abstractmethod
    async def change(self, notification_id: UUID, disabled: bool, user_id: UUID):
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, notification_id: UUID, user_id: UUID):
        raise NotImplementedError
