from datetime import date
from sqlalchemy import and_, func, or_, select
from app.hotels.models import Hotels
from app.service.base import BaseService
from app.database import async_session_maker
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                or_(
                    and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
                    and_(Bookings.date_from <= date_from, Bookings.date_to > date_from)
                )
            ).cte('booked_rooms')
            
            hotels_query = select(
                Hotels.__table__.columns, 
                (
                    func.sum(
                        Rooms.quantity - select(
                            func.count(booked_rooms.c.room_id)
                        ).where(booked_rooms.c.room_id == Rooms.id)
                    )
                ).label('rooms_left')
            ).select_from(Hotels).join(
                Rooms, Rooms.hotel_id == Hotels.id
            ).filter(
                Hotels.location.ilike(f'%{location}%')
            ).group_by(Hotels.id)

            result = await session.execute(hotels_query)
            result_list = []

            for record in result.mappings().all():
                if record['rooms_left'] >= 1:
                    result_list.append(record)
            return result_list
