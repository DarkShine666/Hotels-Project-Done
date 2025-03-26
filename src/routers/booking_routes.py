from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.booking_service import (
    create_booking,
    delete_booking,
    get_bookings_by_room,
)
from src.schemas.booking import BookingCreate, BookingResponse
from src.database import get_db

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/create", response_model=BookingResponse)
async def add_booking(booking: BookingCreate, db: AsyncSession = Depends(get_db)):
    # Создаем новое бронирование
    return await create_booking(db, booking)


@router.delete("/delete/{booking_id}")
async def remove_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    # Удаляем бронирование по ID
    deleted_booking = await delete_booking(db, booking_id)
    if not deleted_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": "Booking deleted"}


@router.get("/list", response_model=list[BookingResponse])
async def list_bookings(room_id: int, db: AsyncSession = Depends(get_db)):
    # Получаем список бронирований для указанного номера
    return await get_bookings_by_room(db, room_id)
