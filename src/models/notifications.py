from enum import Enum
from uuid import UUID

from models.mixins import UUIDMixin


class NotificationChannelTypes(str, Enum):
    email = "email"


# class NotificationRecipient(BaseModel):
#     id: UUID
#     channel: NotificationChannels
#     address: str


class Notification(UUIDMixin):
    template_id: UUID
    channels: list[NotificationChannelTypes]
    context: dict
    title: str
