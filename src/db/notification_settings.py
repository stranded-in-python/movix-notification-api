from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from .abc import NotificationSettingsChannelDBABC, NotificationSettingsDBABC

class NotificationSettingsChannelPSQL(NotificationSettingsChannelDBABC):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def create(self, channel: str, enabled: bool, user_id: UUID) -> None: # неизвестно что при таком раскладе вернет
        if await self.get(user_id, channel):
            return None # или эксепшин что уже существует
        await self.session.execute(
            """
            INSERT INTO notifications.user_settings
            (user, default, email_enabled)
            (:user, :channel, :enabled)
            """,
            {"user": user_id, "channel": channel, "enabled": enabled}
        )
        await self.session.commit()
        return None

    async def get_many(self, user_id: UUID) -> [dict[str, Any]]:
        result = await self.session.execute(
            """
            SELECT default, email_enabled
            FROM notifications.user_settings
            WHERE user = :user_id
            """,
            {"user": user_id}
        )
        return result.fetchall()._asdict()
    
    async def get(self, user_id: UUID, channel: str) -> dict[str, Any]:
        result = await self.session.execute(
            """
            SELECT * from notifications.user_settings
            WHERE user = :user_id AND default = :channel
            """,
            {"user_id": user_id, "channel": channel}
        )
        return result.fetchone()

    async def change(self, channel: str, enabled: bool, user_id: UUID):
        await self.session.execute(
            """
            UPDATE notifications.user_settings
            SET email_enabled = :enabled
            WHERE default = :channel AND
            user = :user_id
            """,
            {"channel": channel, "enabled": enabled, "user_id": user_id}
        )
        await self.session.commit()
    
    async def delete(self, channel: str, user_id: UUID):
        await self.session.execute(
            """
            DELETE FROM notifications.user_settings
            WHERE default = :channel AND user = :user_id
            """,
            {"channel": channel, "user_id": user_id}
        )
        await self.session.commit()

class NotificationSettingsPSQL(NotificationSettingsDBABC):
    def __init__(self):
        pass

    async def create(self, notification_id: UUID, disabled: bool, user_id: UUID):
        if await self.get(user_id, notification_id):
            return None # или эксепшин что уже существует
        await self.session.execute(
            """
            INSERT INTO notifications.notification_settings
            (user, notification, email_disabled)
            (:user_id, :notification_id, :disabled)
            """,
            {"user_id": user_id, "notification_id": notification_id, "disabled": disabled}
        )
        await self.session.commit()
        return None

    async def get(self, user_id: UUID, notification_id: UUID):
        result = await self.session.execute(
            """
            SELECT * from notifications.notification_settings
            WHERE user = :user_id AND notification = :notification_id
            """,
            {"user_id": user_id, "notification_id": notification_id}
        )
        return result.fetchone()

    async def get_many(self, user_id: UUID):
        result = await self.session.execute(
            """
            SELECT notification, email_disabled
            FROM notifications.notification_settings
            WHERE user = :user_id
            """,
            {"user_id": user_id}
        )
        return result.fetchall()._asdict()
    
    async def change(self, notification_id: UUID, disabled: bool, user_id: UUID):
        await self.session.execute(
            """
            UPDATE notifications.notification_settings
            SET email_disabled = :disabled
            WHERE notification = :notification_id
            AND user = :user_id
            """,
            {"notification_id": notification_id, "disabled": disabled, "user_id": user_id}
        )
        await self.session.commit()
    
    async def delete(self, notification_id: UUID, user_id: UUID):
        await self.session.execute(
            """
            DELETE from notifications.notification_settings
            WHERE notification = :notification
            AND user = :user_id
            """,
            {"notification_id": notification_id, "user_id": user_id}
        )
        await self.session.commit()
