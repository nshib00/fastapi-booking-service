from email.message import EmailMessage

from app.config import settings
from pydantic import EmailStr


def setup_email(email: EmailMessage, email_subject: str, email_to: EmailStr) -> None:
    email["Subject"] = email_subject
    email["From"] = settings.SMTP_USER
    email["To"] = email_to


def set_email_content(email: EmailMessage, booking: dict, header: str) -> None:
    email.set_content(
        f"""
            <h1>{header}</h1>
            <p>Вы забронировали номер в отеле {booking["hotel_name"]}.
            <p>Местоположение: {booking["hotel_location"]}.
            <p>Тип номера: {booking["room_name"]}.
            <p>
            Период бронирования: с {booking["date_from"]:%d.%m.%Y} по {booking["date_to"]:%d.%m.%Y}
            (всего дней: {booking["total_days"]}).
            </p>
            <p>Стоимость бронирования: <strong>{booking["total_cost"]} ₽.</strong></p>
            <button type="submit">Подтвердить</button>
        """,
        subtype="html",
    )


def create_booking_confirmation_message(booking: dict, email_to: EmailStr) -> EmailMessage:
    email = EmailMessage()
    setup_email(email, email_to=email_to, email_subject="Подтверждение бронирования")
    set_email_content(email, booking=booking, header="Подтвердите бронирование")
    return email


def create_booking_remind_message(
    booking: dict, email_to: EmailStr, email_subject: str
) -> EmailMessage:
    email = EmailMessage()
    setup_email(email, email_to=email_to, email_subject=email_subject)
    set_email_content(email, booking=booking, header="Напоминаем о заселении")
    return email
