from pathlib import Path
from PIL import Image
from pathlib import Path
import smtplib

from pydantic import EmailStr

from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_message
from app.config import settings


@celery.task
def process_image(path: str) -> None:
    image_path = Path(path)
    image = Image.open(image_path)
    image_ratio = image.width / image.height
    big_resized_image = image.resize(
        (image.height, int(image.height / image_ratio))
    )
    small_resized_image = image.resize(
        (int(image.height / 3), int(image.height / (3 * image_ratio)))
    )
    big_resized_image.save(
        image_path.parent / f'resized-big-{image_path.name}'
    )
    small_resized_image.save(
        image_path.parent / f'resized-small-{image_path.name}'
    )


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr) -> None:
    email = create_booking_confirmation_message(booking, email_to)
    with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp_server:
        smtp_server.login(user=settings.SMTP_USER, password=settings.SMTP_PASS)
        smtp_server.send_message(email)