from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class RoomCreate(BaseModel):
    name: str

class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    is_active: bool
#    owner_id: UUID
    created_at: datetime

class RoomAddParticipant(BaseModel):
    user_id: UUID
