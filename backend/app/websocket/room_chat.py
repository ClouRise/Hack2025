import json
import asyncio
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

# Активные клиенты по комнатам
active_connections: dict[str, list[WebSocket]] = {}
# Задачи слушателей Redis (по комнатам)
room_listeners: dict[str, asyncio.Task] = {}


async def get_user(user_id: str, db: AsyncSession) -> Optional[UserModel]:
    stmt = select(UserModel).where(UserModel.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_room(room_id: str, db: AsyncSession) -> Optional[RoomModel]:
    stmt = select(RoomModel).where(RoomModel.id == room_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def start_room_listener(room_id: str):
    """Один слушатель Redis на комнату"""
    if room_id in room_listeners:
        return  # уже запущен

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(room_id)

    async def listener():
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message:
                    data = json.loads(message["data"])
                    sender_id = data.get("sender_id")
                    # Рассылаем всем участникам комнаты
                    for conn in active_connections.get(room_id, []):
                        # Не отправляем обратно отправителю
                        if conn.headers.get("user_id") != str(sender_id):
                            try:
                                await conn.send_json(data)
                            except Exception:
                                pass
                await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            await pubsub.unsubscribe(room_id)
            await pubsub.close()

    task = asyncio.create_task(listener())
    room_listeners[room_id] = task


@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id: str, db: AsyncSession = Depends(get_async_db)):
    # Сохраняем user_id в headers, чтобы потом фильтровать
    websocket.headers._list.append((b"user_id", str(user_id).encode()))

    await websocket.accept()
    print(f"✅ User {user_id} connected to room {room_id}")

    user = await get_user(user_id, db)
    if not user:
        await websocket.close(code=1008)
        return

    room = await get_room(room_id, db)
    if not room or not room.is_active:
        await websocket.close(code=1008)
        return

    # Добавляем в активные подключения
    active_connections.setdefault(room_id, []).append(websocket)

    # Убедимся, что слушатель для этой комнаты запущен
    await start_room_listener(room_id)

    try:
        while True:
            text = await websocket.receive_text()
            msg = {
                "sender_id": str(user.id),
                "username": getattr(user, "username", str(user.id)),
                "message": text
            }

            # Отправляем СЕБЕ локально сразу (без Redis-задержки)
            await websocket.send_json(msg)

            # Публикуем для других
            await redis_client.publish(room_id, json.dumps(msg))

            # Сохраняем в БД
            db_message = MessageModel(room_id=room.id, user_id=user.id, content=text)
            db.add(db_message)
            await db.commit()
    except WebSocketDisconnect:
        print(f"❌ User {user_id} disconnected from room {room_id}")
    finally:
        if websocket in active_connections.get(room_id, []):
            active_connections[room_id].remove(websocket)
        # Если в комнате больше нет клиентов — останавливаем слушателя
        if not active_connections.get(room_id):
            listener = room_listeners.pop(room_id, None)
            if listener:
                listener.cancel()
