from pydantic import BaseModel

from models.mixins import UUIDMixin


class NotificationPayload(BaseModel):
    mime_type: str
    message: str


class NotificationRecipients(BaseModel):
    email: list[str]


class Notification(UUIDMixin):
    payload: NotificationPayload
    recipients: NotificationRecipients
