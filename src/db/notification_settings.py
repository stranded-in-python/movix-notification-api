from typing import Any, AsyncGenerator
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # noqa
from sqlalchemy.sql import text

from core import exceptions
from core.config import get_database_url_async

from .abc import NotificationSettingsChannelDBABC, NotificationSettingsDBABC


class NotificationSettingsChannelPSQL(NotificationSettingsChannelDBABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, channel: str, enabled: bool, user_id: UUID
    ) -> None | Exception:
        if await self.get(user_id, channel):
            return exceptions.ObjectAlreadyExists()
        await self.session.execute(
            text(
                """
            INSERT INTO notifications.user_settings
            ("user", "default", email_enabled)
            VALUES(:user, :channel, :enabled)
            """
            ),
            {"user": user_id, "channel": channel, "enabled": enabled},
        )
        await self.session.commit()

    async def get_many(self, user_id: UUID) -> list[dict[str, Any]] | None:
        result = await self.session.execute(
            text(
                """
            SELECT "default", email_enabled
            FROM notifications.user_settings
            WHERE "user" = :user_id
            """
            ),
            {"user_id": user_id},
        )
        result = [row._asdict() for row in result.fetchall()]
        if result == []:
            return None
        return result

    async def get(self, user_id: UUID, channel: str) -> dict[str, Any] | None:
        result = await self.session.execute(
            text(
                """
            SELECT * from notifications.user_settings
            WHERE "user" = :user_id AND "default" = :channel
            """
            ),
            {"user_id": user_id, "channel": channel},
        )
        return result.fetchone()

    async def change(self, channel: str, enabled: bool, user_id: UUID) -> None:
        await self.session.execute(
            text(
                """
            UPDATE notifications.user_settings
            SET email_enabled = :enabled
            WHERE "default" = :channel AND
            "user" = :user_id
            """
            ),
            {"channel": channel, "enabled": enabled, "user_id": user_id},
        )
        await self.session.commit()

    async def delete(self, channel: str, user_id: UUID) -> None:
        await self.session.execute(
            text(
                """
            DELETE FROM notifications.user_settings
            WHERE "default" = :channel AND "user" = :user_id
            """
            ),
            {"channel": channel, "user_id": user_id},
        )
        await self.session.commit()


class NotificationSettingsPSQL(NotificationSettingsDBABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ) -> None | Exception:
        if await self.get(user_id, notification_id):
            return exceptions.ObjectAlreadyExists()
        await self.session.execute(
            text(
                """
            INSERT INTO notifications.notification_settings
            ("user", notification, email_disabled)
            VALUES(:user_id, :notification_id, :disabled)
            """
            ),
            {
                "user_id": user_id,
                "notification_id": notification_id,
                "disabled": disabled,
            },
        )
        await self.session.commit()
        return None

    async def get(self, user_id: UUID, notification_id: UUID) -> dict[str, Any] | None:
        result = await self.session.execute(
            text(
                """
            SELECT * from notifications.notification_settings
            WHERE "user" = :user_id AND notification = :notification_id
            """
            ),
            {"user_id": user_id, "notification_id": notification_id},
        )
        return result.fetchone()

    async def get_many(self, user_id: UUID) -> list[dict[str, Any]] | None:
        result = await self.session.execute(
            text(
                """
            SELECT notification, email_disabled
            FROM notifications.notification_settings
            WHERE "user" = :user_id
            """
            ),
            {"user_id": user_id},
        )
        result = [row._asdict() for row in result.fetchall()]
        if result == []:
            return None
        return result

    async def change(
        self, notification_id: UUID, disabled: bool, user_id: UUID
    ) -> None:
        await self.session.execute(
            text(
                """
            UPDATE notifications.notification_settings
            SET email_disabled = :disabled
            WHERE notification = :notification_id
            AND "user" = :user_id
            """
            ),
            {
                "notification_id": notification_id,
                "disabled": disabled,
                "user_id": user_id,
            },
        )
        await self.session.commit()

    async def delete(self, notification_id: UUID, user_id: UUID) -> None:
        await self.session.execute(
            text(
                """
            DELETE from notifications.notification_settings
            WHERE notification = :notification_id
            AND "user" = :user_id
            """
            ),
            {"notification_id": notification_id, "user_id": user_id},
        )
        await self.session.commit()


engine = create_async_engine(get_database_url_async())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_channel_settings_db(session: AsyncSession = Depends(get_async_session)):
    yield NotificationSettingsChannelPSQL(session)


async def get_notifications_settings_db(
    session: AsyncSession = Depends(get_async_session),
):
    yield NotificationSettingsPSQL(session)
