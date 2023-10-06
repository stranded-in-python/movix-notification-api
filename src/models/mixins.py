from uuid import UUID

from pydantic import BaseModel, EmailStr


class UUIDMixin(BaseModel):
    id: UUID


class UserRecipientMixin(BaseModel):
    email: EmailStr
