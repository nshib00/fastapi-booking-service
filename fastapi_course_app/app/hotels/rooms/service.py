from datetime import date

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from sqlalchemy import and_, func, or_, select, text


class RoomsService(BaseService):
    model = Rooms

    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
        price: int | None = None,
        filter_operator: str = "=",
    ):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    or_(
                        and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                        and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                    )
                )
                .cte("booked_rooms")
            )

            dates_delta = (date_to - date_from).days
            query = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.price * dates_delta).label("total_cost"),
                    (
                        func.sum(
                            Rooms.quantity
                            - select(func.count(booked_rooms.c.room_id)).where(
                                booked_rooms.c.room_id == Rooms.id
                            )
                        )
                    ).label("rooms_left"),
                )
                .select_from(Hotels)
                .join(Rooms, Rooms.hotel_id == Hotels.id)
                .filter_by(hotel_id=hotel_id)
                .group_by(Rooms.id)
            )
            if price:
                query = query.filter(text(f"Rooms.price {filter_operator} {price}"))

            result = await session.execute(query)
            result_list = []
            for record in result.mappings().all():
                if record["rooms_left"] >= 1:
                    result_list.append(record)
            return result_list
