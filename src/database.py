from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from typing import AsyncGenerator

# Загрузка переменных окружения из .env
load_dotenv()

# URL для подключения к базе данных (берется из переменной окружения)
DATABASE_URL: str = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не задан в переменных окружения.")


# Создаем движок (engine) для подключения к базе данных
engine = create_async_engine(DATABASE_URL, echo=True)


# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем фабрику сессий
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Функция для получения сессии базы данных
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронная зависимость для получения сессии базы данных.

    Эта функция используется в FastAPI через Depends для предоставления
    асинхронного сеанса работы с базой данных. Сессия автоматически закрывается
    после выхода из контекста.

    Yields:
        AsyncSession: экземпляр асинхронной сессии базы данных.
    """
    async with async_session() as session:
        yield session
