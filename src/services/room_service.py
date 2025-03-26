from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc, desc
from typing import List, Optional

from src.models.room import Room
from src.schemas.room import RoomCreate


async def create_room(db: AsyncSession, room: RoomCreate) -> Room:
    # Создаем новый объект Room на основе переданных данных
    db_room = Room(
        name=room.name,
        description=room.description,
        price_per_night=room.price_per_night,
    )
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room


async def delete_room(db: AsyncSession, room_id: int) -> Optional[Room]:
    # Получаем объект Room по его ID
    result = await db.execute(select(Room).filter(Room.id == room_id))
    db_room = result.scalar_one_or_none()
    if db_room:
        await db.delete(db_room)
        await db.commit()
    return db_room


async def get_rooms(
    db: AsyncSession, sort_by: str = "created_at", order: str = "asc"
) -> List[Room]:
    # Формируем запрос для получения списка номеров с сортировкой
    query = select(Room)
    if sort_by == "price":
        query = (
            query.order_by(asc(Room.price_per_night))
            if order == "asc"
            else query.order_by(desc(Room.price_per_night))
        )
    elif sort_by == "created_at":
        query = (
            query.order_by(asc(Room.created_at))
            if order == "asc"
            else query.order_by(desc(Room.created_at))
        )
    result = await db.execute(query)
    return result.scalars().all()
