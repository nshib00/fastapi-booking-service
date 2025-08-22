from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.bookings.models import Bookings
    from app.hotels.models import Hotels


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    hotel: Mapped["Hotels"] = relationship("Hotels", back_populates="rooms")
    booking: Mapped["Bookings"] = relationship("Bookings", back_populates="room")

    def __str__(self):
        return f"Номер {self.name}"
