from uuid import UUID

from fastapi import Depends

from db.abc import NotificationSettingsChannelDBABC, NotificationSettingsDBABC
from db.notification_settings import (
    get_channel_settings_db,
    get_notifications_settings_db,
)
from models.notification_settings import ChannelSettings, NotificationSettings

from .abc import NotificationChannelSettingsServiceABC, NotificationSettingsServiceABC


class NotificationChannelSettingsService(NotificationChannelSettingsServiceABC):
    def __init__(self, db: NotificationSettingsChannelDBABC):
        self.db = db

    async def create_channel_setting(
        self, channel: str, enabled: bool, user_id: UUID
    ) -> None | Exception:
        return await self.db.create(channel, enabled, user_id)

    async def get_channel_settings(self, user_id: UUID) -> list[ChannelSettings] | None:
        settings = await self.db.get_many(user_id)
        if settings is not None:
            return [ChannelSettings(**row) for row in settings]
        return None

    async def change_channel_settings(
        self, channel: str, enabled: bool, user_id: UUID
    ) -> None:
        await self.db.change(channel, enabled, user_id)

    async def delete_channel_settings(self, channel: str, user_id: UUID) -> None:
        await self.db.delete(channel, user_id)


class NotificationSettingsService(NotificationSettingsServiceABC):
    def __init__(self, db: NotificationSettingsDBABC):
        self.db = db

    async def create_notification_setting(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ) -> None | Exception:
        return await self.db.create(notification_id, disabled, user_id)

    async def get_notification_settings(
        self, user_id: UUID
    ) -> list[NotificationSettings] | None:
        settings = await self.db.get_many(user_id)
        if settings is not None:
            return [NotificationSettings(**row) for row in settings]
        return None

    async def change_notification_settings(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ):
        await self.db.change(notification_id, disabled, user_id)

    async def delete_notification_settings(self, notification_id: UUID, user_id: UUID):
        await self.db.delete(notification_id, user_id)


async def get_channel_settings_service(
    notification_db: NotificationSettingsChannelDBABC = Depends(
        get_channel_settings_db
    ),
) -> NotificationChannelSettingsService:
    yield NotificationChannelSettingsService(notification_db)


async def get_notification_settings_service(
    notification_db: NotificationSettingsDBABC = Depends(get_notifications_settings_db),
) -> NotificationSettingsService:
    yield NotificationSettingsService(notification_db)
