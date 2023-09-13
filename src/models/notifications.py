from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from models.mixins import UUIDMixin


class NotificationChannels(str, Enum):
    email = "email"


class NotificationRecipient(BaseModel):
    id: UUID
    channel: NotificationChannels
    address: str


class Notification(UUIDMixin):
    template_id: UUID
    channels: list[NotificationChannels]
    context: dict
