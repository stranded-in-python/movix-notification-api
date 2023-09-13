from uuid import UUID

from pydantic import BaseModel, EmailStr


class NotificationChannel(BaseModel):
    type: str  # Type of the notification channel
    value: str  # Value of the notification channel


class UserChannels(BaseModel):
    id: str  # ID of the user
    channels: list[NotificationChannel]


class User(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    is_admin: bool = False
    is_verified: bool = False
