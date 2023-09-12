from uuid import UUID

from .abc import (NotificationChannelSettingsServiceABC,
                  NotificationSettingsServiceABC)
from db.abc import NotificationSettingsChannelDBABC, NotificationSettingsDBABC
from models.notification_settings import ChannelSettings, NotificationSettings

class NotificationChannelSettingsService(NotificationChannelSettingsServiceABC):
    def __init__(self, db: NotificationSettingsChannelDBABC):
        self.db = db

    async def create_channel_setting(self, channel: str, enabled: bool, user_id: UUID):
        await self.db.create(channel, enabled, user_id)

    async def get_channel_settings(self, user_id: UUID):
        settings = await self.db.get_many(user_id)
        return [ChannelSettings(**row) for row in settings]

    async def change_channel_settings(self, channel: str, enabled: bool, user_id: UUID):
        await self.db.change(channel, enabled, user_id)

    async def delete_channel_settings(self, channel: str, user_id: UUID):
        await self.db.delete(channel, user_id)


class NotificationSettingsService(NotificationSettingsServiceABC):
    def __init__(self, db: NotificationSettingsDBABC):
        self.db = db

    async def create_notification_setting(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        await self.db.create(notification_id, disabled, user_id, UUID)

    async def get_notification_settings(self, user_id: UUID):
        await self.db.get_many(user_id)

    async def change_notification_settings(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        await self.db.change(notification_id, disabled, user_id)

    async def delete_notification_settings(self, notification_id: UUID, user_id: UUID):
        await self.db.delete(notification_id, user_id)


def get_channel_settings():
    return NotificationChannelSettingsService()

def get_notification_settings():
    return NotificationSettingsService()
