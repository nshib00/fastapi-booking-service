from datetime import date
from fastapi import APIRouter, Depends
import sys
from pathlib import Path

from app.exceptions import RoomCannotBeBookedException


app_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(app_path))

from app.bookings.schemas import BookingsSchema
from app.bookings.service import BookingsService
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(prefix='/bookings', tags=['Бронирования'])


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)): # -> list[BookingsSchema]:
    return await BookingsService.find_all(user_id=user.id)


@router.post('')
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    new_booking = await BookingsService.add(user.id, room_id, date_from, date_to)
    if new_booking is None:
        raise RoomCannotBeBookedException

