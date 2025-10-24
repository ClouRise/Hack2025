from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from backend.app.schemas.user import UserRead

class MessageCreate(BaseModel):
    room_id: UUID
    sender_id: UUID
    content: str

class MessageRead(BaseModel):
    id: int
    room_id: UUID
    sender: UUID
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True
