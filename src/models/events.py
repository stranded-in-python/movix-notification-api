from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserOnRegistration(BaseModel):
    email: EmailStr
    verification_token: str
    id_user: UUID
