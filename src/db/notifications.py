import typing as t

from db.models_protocol import ID, NP, SP, TCP, TP


class BaseNotificationDatabase(t.Generic[ID, NP, TP, TCP]):
    """Base adapter for retrieving notifications from a database."""

    async def get_notification(self, ID) -> NP | None:
        """Get a notification data"""
        raise NotImplementedError

    async def get_template_data(self, ID) -> TP | None:
        """Get a template data"""
        raise NotImplementedError

    async def get_template_data_with_context(self, ID) -> TCP | None:
        """Get a temlate data with context"""
        raise NotImplementedError

    async def get_notifications_scheduler_data(self, ID) -> SP | None:
        """Get a notifications scheduler data"""


class SANotificationDB(BaseNotificationDatabase):
    ...
