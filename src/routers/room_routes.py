from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.room_service import create_room, delete_room, get_rooms
from src.schemas.room import RoomCreate, RoomResponse
from src.database import get_db

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("/", response_model=RoomResponse)
async def add_room(room: RoomCreate, db: AsyncSession = Depends(get_db)):
    # Создаем новый номер
    return await create_room(db, room)


@router.delete("/{room_id}")
async def remove_room(room_id: int, db: AsyncSession = Depends(get_db)):
    # Удаляем номер по ID
    deleted_room = await delete_room(db, room_id)
    if not deleted_room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted"}


@router.get("/", response_model=list[RoomResponse])
async def list_rooms(
    sort_by: str = "created_at", order: str = "asc", db: AsyncSession = Depends(get_db)
):
    # Получаем список номеров с возможностью сортировки
    return await get_rooms(db, sort_by, order)
