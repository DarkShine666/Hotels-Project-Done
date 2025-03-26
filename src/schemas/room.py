from pydantic import BaseModel
from datetime import datetime


# Схема для создания нового номера
class RoomCreate(BaseModel):
    name: str
    description: str
    price_per_night: float


# Схема для ответа при получении информации о номере
class RoomResponse(BaseModel):
    id: int
    name: str
    description: str
    price_per_night: float
    created_at: datetime

    class Config:
        orm_mode = True
