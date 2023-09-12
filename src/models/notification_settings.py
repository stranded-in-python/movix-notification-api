from uuid import UUID

from .mixins import BaseModel


class ChannelSettings(BaseModel):
    channel: str
    email_enabled: bool


class NotificationSettings(BaseModel):
    notification: UUID
    email_disabled: bool
