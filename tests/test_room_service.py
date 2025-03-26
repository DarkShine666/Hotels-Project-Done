import os
from dotenv import load_dotenv
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.schemas.room import RoomCreate
from src.services.room_service import create_room, delete_room, get_rooms

# Загружаем переменные окружения
load_dotenv()

# Читаем URL тестовой базы данных из переменной окружения
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL не задан в переменных окружения")


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_room(async_session: AsyncSession):
    room_data = RoomCreate(name="101", description="Deluxe Room", price_per_night=120.0)
    room = await create_room(async_session, room_data)
    assert room.id is not None
    assert room.name == room_data.name
    assert room.price_per_night == room_data.price_per_night


@pytest.mark.asyncio
async def test_delete_room(async_session: AsyncSession):
    room_data = RoomCreate(
        name="102", description="Standard Room", price_per_night=80.0
    )
    room = await create_room(async_session, room_data)
    room_id = room.id
    deleted_room = await delete_room(async_session, room_id)
    assert deleted_room is not None
    # Повторное удаление должно вернуть None
    deleted_again = await delete_room(async_session, room_id)
    assert deleted_again is None


@pytest.mark.asyncio
async def test_get_rooms(async_session: AsyncSession):
    # Создаем два номера
    room_data1 = RoomCreate(name="103", description="Suite", price_per_night=200.0)
    room_data2 = RoomCreate(name="104", description="Economy", price_per_night=50.0)
    await create_room(async_session, room_data1)
    await create_room(async_session, room_data2)

    # Проверяем сортировку по цене (asc)
    rooms = await get_rooms(async_session, sort_by="price", order="asc")
    assert rooms[0].price_per_night <= rooms[1].price_per_night

    # Проверяем сортировку по дате создания (desc)
    rooms = await get_rooms(async_session, sort_by="created_at", order="desc")
    assert rooms[0].created_at >= rooms[1].created_at
