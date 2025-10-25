from fastapi import APIRouter
from livekit.api import AccessToken, VideoGrants
from pydantic import BaseModel
from typing import Optional
import json

router = APIRouter(
    prefix="/liveKit",
    tags=["liveKit"]
)

LIVEKIT_KONFIG = {
    "host": "185.31.164.246",
    "port": 7880,
    "api_key": "hack2025",
    "secret_key": "secret_hack2025"
}

class TokenRequest(BaseModel):
    room_name: str 
    user_id: int
    user_name: Optional[str] = None

@router.post('/api/get-token')
async def create_token(request: TokenRequest):
    api_key = LIVEKIT_KONFIG["api_key"]
    secret_key = LIVEKIT_KONFIG["secret_key"]
    db_url = f"{LIVEKIT_KONFIG['host']}:{LIVEKIT_KONFIG['port']}"

    token = AccessToken(
        api_key=api_key,
        api_secret=secret_key
    )

    grant = VideoGrants(room=request.room_name, room_join=True, can_publish=True, can_subscribe=True)

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