from datetime import datetime
from enum import Enum
from typing import Protocol, TypeVar
from uuid import UUID

ID = TypeVar("ID")


class MessageType(str, Enum):
    idle = "idle"
    processing = "processing"


class NotifiacationProtocol(Protocol[ID]):
    id: ID
    template_id: UUID
    channels: list[str]
    users: list[ID]


class TemplateProtocol(Protocol[ID]):
    id: UUID
    mime_type: str
    context_id: UUID
    body: bytes


class TemlateContextProtocol(TemplateProtocol):
    varibles: list[str]


class SchedulerProtocol(Protocol[ID]):
    id: ID
    notification_id: ID
    status: MessageType
    priority: int
    cron: str
    scheduled_at: datetime


NP = TypeVar("NP", bound=NotifiacationProtocol[UUID])
TP = TypeVar("TP", bound=TemplateProtocol[UUID])
TCP = TypeVar("TCP", bound=TemlateContextProtocol[UUID])
SP = TypeVar("SP", bound=SchedulerProtocol[UUID])
