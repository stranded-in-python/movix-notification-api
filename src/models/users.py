from pydantic import BaseModel


class UserSettings(BaseModel):
    id: str  # ID of the notification channel
    type: str  # Type of the notification channel
    value: str  # Value of the notification channel
