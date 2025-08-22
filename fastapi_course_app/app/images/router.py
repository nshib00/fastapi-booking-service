import shutil

from app.tasks.tasks import process_image
from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/hotels", status_code=201)
async def load_hotel_image(name: int, file: UploadFile):
    image_path = f"fastapi_course_app/app/static/images/{name}.webp"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
    process_image.delay(path=image_path)
