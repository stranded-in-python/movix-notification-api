from enum import Enum
from typing import Any, OrderedDict
from uuid import UUID

from pydantic import BaseModel

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
    context_vars: dict
    title: str


class UserContext(BaseModel):
    user_id: UUID
    context: OrderedDict[str, Any]


class GroupedContext(BaseModel):
    user_ids: list[UUID]
    context: OrderedDict[str, Any]
