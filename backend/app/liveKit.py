from fastapi import APIRouter, Depends, HTTPException, status
from livekit.api import AccessToken, VideoGrants
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, validator, Field
import uuid
from typing import Optional
from app.db_depends import get_async_db
import os

from app.models.users import User
from app.models.rooms import Room

router = APIRouter(
    prefix="/liveKit",
    tags=["liveKit"]
)

# LIVEKIT_KONFIG = {
#     "host": "185.31.164.246",
#     "port": 7880,
#     "api_key": "hack2025",
#     "secret_key": "secret_hack2025"
# }

class TokenRequest(BaseModel):
    room_id: str
    user_id: str
    user_name: str
    @validator("room_id", pre=False) #только после основной валидации
    def validate_uuid(cls, value_room):
        try:
            return uuid.UUID(value_room)
        except ValueError:
            raise ValueError("This value dont validate")
        
    @validator("user_id", pre=False)
    def validate_user(cls, value_user):
        try:
            return uuid.UUID(value_user)
        except ValueError:
            raise ValueError("This value dont validate")
        
class GuestToken(BaseModel):
    room_id: str
    user_id: str
    user_name: Optional[str] = Field(default='guest')

    @validator("room_id", pre=False) #только после основной валидации
    def validate_uuid(cls, value_room):
        try:
            return uuid.UUID(value_room)
        except ValueError:
            raise ValueError("This value dont validate")
        
    @validator("user_id", pre=False)
    def validate_user(cls, value_user):
        try:
            return uuid.UUID(value_user)
        except ValueError:
            raise ValueError("This value dont validate")


@router.post('/api/get-token')
async def create_token(request: TokenRequest, db: AsyncSession = Depends(get_async_db)):
    # api_key = LIVEKIT_KONFIG["api_key"]
    # secret_key = LIVEKIT_KONFIG["secret_key"]
    # db_url = f"{LIVEKIT_KONFIG['host']}:{LIVEKIT_KONFIG['port']}"
    api_key = os.getenv("LIVEKIT_KONFIG_API_KEY")
    secret_key = os.getenv("LIVEKIT_KONFIG_SECRET_API_KEY")
    db_host = os.getenv("LIVEKIT_KONFIG_HOST")
    db_port = os.getenv("LIVEKIT_KONFIG_PORT")
    db_url = f"{db_host}:{db_port}"

    token = AccessToken(
        api_key=api_key,
        api_secret=secret_key
    )

    nice_uuid_room = select(Room).where(Room.id == request.room_id).where(Room.is_active == True)
    if nice_uuid_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room by {request.uuid_room} not found"
        )

    grant = VideoGrants(room=str(request.room_id), room_join=True, can_publish=True, can_subscribe=True)

    token.with_grants(grant)

    token.with_name(str(request.user_name))
    token.with_identity(str(request.user_id))

    # token.identity = json.dumps(request.user_id)
    # token.name = json.dumps(request.user_name)
    jwt = token.to_jwt()

    return {
        "token": jwt,
        "db_url": db_url
    }

@router.post('/api/get-token-for-guest')
async def create_token_for_guest(request: GuestToken):
    api_key = os.getenv("LIVEKIT_KONFIG_API_KEY")
    secret_key = os.getenv("LIVEKIT_KONFIG_SECRET_API_KEY")
    db_host = os.getenv("LIVEKIT_KONFIG_HOST")
    db_port = os.getenv("LIVEKIT_KONFIG_PORT")
    db_url = f"{db_host}:{db_port}"

    token = AccessToken(
        api_key=api_key,
        api_secret=secret_key
    )

    grant = VideoGrants(room=str(request.room_id), room_join=True, can_subscribe=True)

    token.with_grants(grant)

    token.with_name(str(request.user_name))
    token.with_identity(str(request.user_id))

    jwt = token.to_jwt()

    return {
        "token": jwt,
        "db_url": db_url
    }