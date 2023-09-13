from pydantic import BaseModel


class NotificationChannel(BaseModel):
    type: str  # Type of the notification channel
    value: str  # Value of the notification channel


class UserChannels(BaseModel):
    id: str  # ID of the user
    channels: list[NotificationChannel]


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    is_active: bool
    is_verified: bool
