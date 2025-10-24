from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    room: UUID


    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

