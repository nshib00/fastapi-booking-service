import shutil
from fastapi import APIRouter, UploadFile


router = APIRouter(prefix='/images', tags=['Загрузка картинок'])


@router.post('/hotels', status_code=201)
async def load_hotel_image(name: int, file: UploadFile):
    with open(f'fastapi_course_app/app/static/images/{name}.webp', 'wb+') as new_file:
        shutil.copyfileobj(file.file, new_file)

