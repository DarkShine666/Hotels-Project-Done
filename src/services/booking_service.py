from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.booking import Booking
from src.schemas.booking import BookingCreate
from typing import List, Optional


async def create_booking(db: AsyncSession, booking: BookingCreate) -> Booking:
    db_booking = Booking(
        room_id=booking.room_id,
        date_start=booking.date_start,
        date_end=booking.date_end,
    )
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking


async def delete_booking(db: AsyncSession, booking_id: int) -> Optional[Booking]:
    # Выполняем запрос для получения бронирования по ID
    result = await db.execute(select(Booking).filter(Booking.id == booking_id))
    db_booking = result.scalar_one_or_none()
    if db_booking:
        await db.delete(db_booking)
        await db.commit()
    return db_booking


async def get_bookings_by_room(db: AsyncSession, room_id: int) -> List[Booking]:
    result = await db.execute(
        select(Booking).filter(Booking.room_id == room_id).order_by(Booking.date_start)
    )
    bookings = result.scalars().all()
    return bookings
