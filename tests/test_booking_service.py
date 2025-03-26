import os
from dotenv import load_dotenv
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.schemas.room import RoomCreate
from src.schemas.booking import BookingCreate
from src.services.room_service import create_room
from src.services.booking_service import (
    create_booking,
    delete_booking,
    get_bookings_by_room,
)

load_dotenv()
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5433/test_db"
)
if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL не задан в переменных окружения")


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_create_booking(async_session: AsyncSession):
    # Создаем комнату, чтобы ее id существовал
    room_data = RoomCreate(name="Test Room", description="Test", price_per_night=100.0)
    room = await create_room(async_session, room_data)

    # Используем id созданной комнаты
    booking_data = BookingCreate(
        room_id=room.id, date_start="2023-01-01", date_end="2023-01-05"
    )
    booking = await create_booking(async_session, booking_data)
    assert booking.id is not None
    assert booking.room_id == room.id


@pytest.mark.asyncio
async def test_delete_booking(async_session: AsyncSession):
    # Создаем комнату
    room_data = RoomCreate(name="Test Room", description="Test", price_per_night=100.0)
    room = await create_room(async_session, room_data)

    booking_data = BookingCreate(
        room_id=room.id, date_start="2023-01-01", date_end="2023-01-05"
    )
    booking = await create_booking(async_session, booking_data)
    booking_id = booking.id

    deleted_booking = await delete_booking(async_session, booking_id)
    assert deleted_booking is not None

    deleted_again = await delete_booking(async_session, booking_id)
    assert deleted_again is None


@pytest.mark.asyncio
async def test_get_bookings_by_room(async_session: AsyncSession):
    # Создаем комнату
    room_data = RoomCreate(name="Test Room", description="Test", price_per_night=100.0)
    room = await create_room(async_session, room_data)

    booking_data1 = BookingCreate(
        room_id=room.id, date_start="2023-01-01", date_end="2023-01-05"
    )
    booking_data2 = BookingCreate(
        room_id=room.id, date_start="2023-01-06", date_end="2023-01-10"
    )
    await create_booking(async_session, booking_data1)
    await create_booking(async_session, booking_data2)

    bookings = await get_bookings_by_room(async_session, room_id=room.id)
    assert isinstance(bookings, list)
    assert len(bookings) == 2
    assert bookings[0].date_start <= bookings[1].date_start
