from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: int = Column(Integer, primary_key=True, index=True)
    room_id: int = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    date_start: Date = Column(Date, nullable=False)
    date_end: Date = Column(Date, nullable=False)

    room = relationship("Room", back_populates="bookings")

    def __repr__(self) -> str:
        return (
            f"Booking(id={self.id}, room_id={self.room_id}, "
            f"date_start={self.date_start}, date_end={self.date_end})"
        )
