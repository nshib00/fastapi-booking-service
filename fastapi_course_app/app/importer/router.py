import csv
import io
from typing import Literal

from app.bookings.service import BookingsService
from app.exceptions import IncorrectTableNameException
from app.hotels.rooms.service import RoomsService
from app.hotels.service import HotelsService
from app.importer.utils import normalize_row
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi import APIRouter, Depends, File, UploadFile

router = APIRouter(prefix='/import', tags=['Импорт данных'])


@router.post('/csv/{table_name}')
async def import_data_from_csv(
    table_name: Literal['hotels', 'rooms', 'bookings'],
    csv_file: UploadFile = File(...),
    user: Users = Depends(get_current_user)
) -> None:
    file_content = await csv_file.read()
    decoded = io.StringIO(file_content.decode('utf-8'))
    reader = csv.DictReader(decoded, delimiter=';')

    file_data: list[dict] = [normalize_row(row) for row in reader]

    match table_name:
        case 'hotels':
            await HotelsService.add_many(file_data)
        case 'rooms':
            await RoomsService.add_many(file_data)
        case 'bookings':
            await BookingsService.add_many(file_data)
        case _:
            raise IncorrectTableNameException
