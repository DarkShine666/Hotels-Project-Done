from fastapi import FastAPI
from src.database import engine, Base
from src.routers.room_routes import router as room_router
from src.routers.booking_routes import router as booking_router
import uvicorn
import os

app = FastAPI(title="Hotel Booking Service (Async)")


# При запуске приложения создаем таблицы, если они еще не созданы
@app.on_event("startup")
async def on_startup():
    # Открываем асинхронное соединение и выполняем синхронную функцию создания таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Регистрируем роутеры
app.include_router(room_router)
app.include_router(booking_router)


# Простой эндпоинт для проверки работы сервиса
@app.get("/")
async def root():
    return {"message": "Welcome to the Hotel Booking Service (Async)!"}


if __name__ == "__main__":
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=True)
