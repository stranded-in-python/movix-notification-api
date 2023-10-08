from uuid import UUID

from pydantic import BaseModel, Field


class ChannelSettings(BaseModel):
    channel: str = Field(alias="default")
    email_enabled: bool


class NotificationSettings(BaseModel):
    notification: UUID
    email_disabled: bool
