from pydantic import BaseModel
from datetime import date


# Схема для создания нового бронирования
class BookingCreate(BaseModel):
    room_id: int
    date_start: date
    date_end: date


# Схема для ответа при получении информации о бронировании
class BookingResponse(BaseModel):
    id: int
    room_id: int
    date_start: date
    date_end: date

    class Config:
        orm_mode = True  # Разрешает работу с SQLAlchemy-моделями
