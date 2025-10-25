from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: EmailStr
    room: UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str

