from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    is_active: bool
    room_id: UUID | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

