from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, root_validator


class Recipients(BaseModel):
    ...


class MessageType(str, Enum):
    email = "email"


class EmailTitle(BaseModel):
    to_: list[EmailStr]
    from_: EmailStr
    subject_: str


class Message(BaseModel):
    context: dict
    template_id: UUID
    type: MessageType
    recipients: EmailTitle

    @root_validator
    def recipients_must_match_type(cls, values):
        recipients = values.get("recipients")
        _type = values.get("_type")

        if _type == MessageType.email:
            if not isinstance(recipients, EmailTitle):
                raise ValueError("recipients do not match type of message")

        return values
