from pydantic import BaseModel, EmailStr


class UserOnRegistration(BaseModel):
    email: EmailStr
    confirm_url: str
