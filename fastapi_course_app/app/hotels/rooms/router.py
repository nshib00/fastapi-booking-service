from fastapi import APIRouter, Depends
from app.hotels.rooms.service import RoomsService
from app.hotels.rooms.schemas import RoomsSchema, RoomsSearchArgs


router = APIRouter(prefix='/hotels', tags=['Комнаты отелей'])


@router.get('/{hotel_id}/rooms')
async def get_hotel_rooms(hotel_id: int, search_args: RoomsSearchArgs = Depends()): # -> list[RoomsSchema]:
    return await RoomsService.find_all(hotel_id, **search_args.__dict__)
