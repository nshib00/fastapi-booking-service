from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.hotels.schemas import HotelsSchema, HotelsSchemaWithRoomsLeft, HotelsSearchArgs
from app.hotels.service import HotelsService
from app.exceptions import DateFromBiggerThanDateToException, HotelNotExistsError


router = APIRouter(tags=['Отели'], prefix='/hotels')


@router.get('/{location}')
@cache(expire=3600)
async def get_hotels(location: str, search_args: HotelsSearchArgs = Depends()) -> list[HotelsSchemaWithRoomsLeft]:
    if search_args.date_from > search_args.date_to:
        raise DateFromBiggerThanDateToException
    return await HotelsService.find_all(location, **search_args.__dict__)


@router.get('/id/{hotel_id}')
async def get_hotel_by_id(hotel_id: int) -> HotelsSchema:
    result_hotel = await HotelsService.find_by_id(hotel_id)
    if result_hotel is None:
        raise HotelNotExistsError
    return result_hotel
