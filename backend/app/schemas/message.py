from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class MessageCreate(BaseModel):
    room_id: UUID
    user_id: UUID
    content: str

class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: UUID
    user_id: UUID
    content: str
    created_at: datetime

