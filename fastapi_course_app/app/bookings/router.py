from datetime import date
from fastapi import APIRouter, Depends
from pydantic import TypeAdapter

from app.bookings.schemas import BookingsResponseSchema
from app.bookings.service import BookingsService
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import RoomCannotBeBookedException
from fastapi_course_app.app.tasks.tasks import send_booking_confirmation_email


router = APIRouter(prefix='/bookings', tags=['Бронирования'])



@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)): # -> list[BookingsResponseSchema]:
    return await BookingsService.find_all(user_id=user.id)


@router.post('')
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    new_booking_id = await BookingsService.add(user.id, room_id, date_from, date_to)
    if new_booking_id is None:
        raise RoomCannotBeBookedException
    new_booking = await BookingsService.find_by_id(booking_id=new_booking_id)
    new_booking_dict = TypeAdapter(dict).validate_python(new_booking)
    send_booking_confirmation_email.delay(booking=new_booking_dict, email_to=user.email)

@router.delete('/{booking_id}', status_code=204)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    return await BookingsService.delete(model_id=booking_id)

