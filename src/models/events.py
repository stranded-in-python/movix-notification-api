from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Events(str, Enum):
    on_registration = "on_registration"


class UserOnRegistration(BaseModel):
    email: EmailStr
    verification_token: str
    id_user: UUID
