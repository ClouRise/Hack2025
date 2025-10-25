import json
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.rooms import Room as RoomModel
from app.models.users import User as UserModel
from app.models.messages import Message as MessageModel
from app.db_depends import get_async_db

router = APIRouter()

REDIS_URL = "redis://localhost:6379"
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# В памяти подключенные вебсокеты по комнате
active_connections: dict[str, list[WebSocket]] = {}

async def get_user(user_id: str, db: AsyncSession) -> Optional[UserModel]:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_room(room_id: str, db: AsyncSession) -> Optional[RoomModel]:
    stmt = select(RoomModel).where(RoomModel.id == room_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str, db: AsyncSession = Depends(get_async_db)):
    await websocket.accept()
    
    user = await get_user(user_id, db)
    if user is None:
        await websocket.close(code=1008)
        return

    room = await get_room(room_id, db)
    if room is None or not room.is_active:
        await websocket.close(code=1008)
        return

    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

    # Подписка на Redis канал комнаты
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(room_id)

    import asyncio

    async def redis_listener():
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                # Отправляем всем подключенным вебсокетам
                for connection in active_connections.get(room_id, []):
                    await connection.send_json(data)

    listener_task = asyncio.create_task(redis_listener())

    try:
        while True:
            data = await websocket.receive_text()
            message_data = {
                "user_id": str(user.id),
                "username": getattr(user, "username", "Guest"),
                "message": data
            }
            # Отправка в Redis
            await redis_client.publish(room_id, json.dumps(message_data))

            # Сохранение в базу данных
            db_message = MessageModel(
                room_id=room.id,
                user_id=user.id,
                content=data
            )
            db.add(db_message)
            await db.commit()
            await db.refresh(db_message)

    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)
        listener_task.cancel()
    except Exception as e:
        active_connections[room_id].remove(websocket)
        listener_task.cancel()
        await websocket.close()
