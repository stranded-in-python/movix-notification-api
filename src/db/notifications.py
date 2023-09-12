import typing as t
from typing import AsyncGenerator
from uuid import UUID

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # noqa

from core.config import get_database_url_async
from db.models_protocol import ID, NP
from models.notifications import Notification


class BaseNotificationDatabase(t.Generic[ID, NP]):
    """Base adapter for retrieving notifications from a database."""

    async def get_notification(self, notification_id: ID) -> NP | None:
        """Get a notification data"""
        raise NotImplementedError

    async def get_notification_users(
        self, notification_id: ID, offset: int
    ) -> AsyncGenerator[list[UUID], None]:
        """Get a notification users"""
        raise NotImplementedError


class SANotificationDB(BaseNotificationDatabase[UUID, Notification]):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session
        self.pack_size = 1000

    async def get_notification(self, notification_id: UUID) -> Notification | None:
        """Get a notification data"""
        query_text = text(
            """
            WITH notification_data AS (
                SELECT id, template_id, created_at, channels
                FROM notifications.notification
                WHERE id = :notification_id
            ),
            notification_template_data AS (
                SELECT notification_data.*, template.context_id
                FROM notification_data
                INNER JOIN notifications.template ON notification_data.template_id = template.id
            ),
            notification_data_with_context AS (
                SELECT notification_template_data.*, context.context_vars
                FROM notification_template_data
                INNER JOIN notifications.context ON notification_template_data.context_id = context.id
            )
            SELECT * FROM notification_data_with_context;
            """
        )
        query_params = {"notification_id": notification_id}

        result = await self.session.execute(query_text, query_params)
        if result.rowcount == 0:
            return None

        row = result.fetchone()

        notification = Notification(
            id=row.id,
            template_id=row.template_id,
            channels=row.channels,
            context=row.context_vars,
        )

        return notification

    async def get_notification_users(
        self, notification_id: UUID, users_limit: int
    ) -> AsyncGenerator[list[UUID], None]:
        """Get a notification users"""
        query_text = """
        WITH notification_data AS (
            SELECT recipients_id
            FROM notifications.notification
            WHERE id = :notification_id
        )
        SELECT user_group_membership.user_id
        FROM notification_data
        INNER JOIN notifications.user_group_membership
        ON notification_data.recipients_id = user_group_membership.group_id
        ORDER BY user_group_membership.user_id;
        """
        query_params = {"notification_id": notification_id}

        result = await self.session.execute(query_text, query_params)
        result_not_empty = True

        while result_not_empty:
            users_ids = []

            while len(users_ids) < users_limit or result_not_empty:

                rows = result.fetchmany(self.pack_size)
                if len(rows) == 0:
                    result_not_empty = False

                users_ids.extend(row[0] for row in rows)

            yield users_ids


engine = create_async_engine(get_database_url_async())
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_notification_db(session: AsyncSession = Depends(get_async_session)):
    yield SANotificationDB(session)
