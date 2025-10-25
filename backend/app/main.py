from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import messages, rooms, users
from app.websocket import room_chat


from app.websocket import room_chat
from app.routers import messages
from app.routers import rooms
from app import liveKit
from pathlib import Path 
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="FastAPI конфа",
    version="0.1.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       #Разрешить все домены   
    allow_credentials=True,    # Разрешить куки и авторизацию
    allow_methods=["*"],       # Разрешить все HTTP методы
    allow_headers=["*"],       # Разрешить все заголовки
    expose_headers=["*"],
)

#ПРИЛОЖЕНИЕ FASTAPI
app.include_router(room_chat.router)
app.include_router(messages.router)
app.include_router(rooms.router)
# app.include_router(liveKit.router)
app.include_router(users.router)

#КОРНЕВОЙ ЭНДПОИНТ 
@app.get("/")
async def root():
    """
    КОРНЕВОЙ МАРШРУТ, ДЛЯ ПРОВЕРКИ API
    """
    return {"message": "ДОБРО ПОЖАЛОВАТЬ"}

@app.get("/test_ws", response_class=HTMLResponse)
async def test_ws():
    file_path = Path(__file__).parent / "templates/ws_test.html"
    return file_path.read_text(encoding="utf-8")