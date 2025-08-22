from app.tasks.celery import celery
from app.tasks.email_smtp import send_email_via_smtp
from app.tasks.email_templates import create_booking_remind_message
from pydantic import EmailStr


@celery.task(name="booking_1_day")
def remind_about_booking_1_day(booking: dict, email_to: EmailStr) -> None:
    email = create_booking_remind_message(
        booking=booking, email_to=email_to, email_subject="Остался 1 день до заселения"
    )
    send_email_via_smtp(email)


@celery.task(name="booking_3_days")
def remind_about_booking_3_days(booking: dict, email_to: EmailStr) -> None:
    email = create_booking_remind_message(
        booking=booking, email_to=email_to, email_subject="Осталось 3 дня до заселения"
    )
    send_email_via_smtp(email)
