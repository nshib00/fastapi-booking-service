from datetime import date

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.exceptions import RoomNotExistsException
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from sqlalchemy import and_, func, insert, or_, select


class BookingsService(BaseService):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                            and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            rooms_left_query = (
                select((Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left"))
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            rooms_left_result = await session.execute(rooms_left_query)
            rooms_left: int | None = rooms_left_result.scalar()

            if rooms_left is None:
                raise RoomNotExistsException

            if rooms_left > 0:
                price_query = select(Rooms.price).filter_by(id=room_id)
                price_result = await session.execute(price_query)
                price: int = price_result.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings.id)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
            else:
                return None

    @classmethod
    def __get_bookings_join(cls, join_hotels=False):
        if join_hotels:
            return (
                select(
                    Bookings.__table__.columns,
                    Rooms.image_id.label("room_image_id"),
                    Rooms.name.label("room_name"),
                    Hotels.name.label("hotel_name"),
                    Hotels.location.label("hotel_location"),
                )
                .select_from(Bookings)
                .join(Rooms, Bookings.room_id == Rooms.id)
                .join(Hotels, Rooms.hotel_id == Hotels.id)
            )
        return (
            select(
                Bookings.__table__.columns,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
            )
            .select_from(Bookings)
            .join(Rooms, Bookings.room_id == Rooms.id)
        )

    @classmethod
    async def find_all(cls, user_id: int):
        async with async_session_maker() as session:
            bookings_query = cls.__get_bookings_join().where(Bookings.user_id == user_id)
            result = await session.execute(bookings_query)
            return result.mappings().all()

    @classmethod
    async def find_by_id(cls, booking_id: int):
        async with async_session_maker() as session:
            bookings_query = cls.__get_bookings_join(join_hotels=True).where(
                Bookings.id == booking_id
            )
            result = await session.execute(bookings_query)
            return result.mappings().one_or_none()
