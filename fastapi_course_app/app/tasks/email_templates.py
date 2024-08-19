from email.message import EmailMessage
from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_message(booking: dict, email_to: EmailStr) -> EmailMessage:
    email = EmailMessage()

    email['Subject'] = 'Подтвердите бронирование отеля'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to

    email.set_content(f'''
            <h1>Подтвердите бронирование</h1>
            <p>Вы забронировали номер в отеле {booking["hotel_name"]}.
            <p>Местоположение: {booking["hotel_location"]}.
            <p>Тип номера: {booking["room_name"]}.
            <p>
            Период бронирования: с {booking["date_from"]:%d.%m.%Y} по {booking["date_to"]:%d.%m.%Y} (всего дней: {booking["total_days"]}).
            </p>
            <p>Стоимость бронирования: <strong>{booking["total_cost"]} ₽.</strong></p>
            <button type="submit">Подтвердить</button>
        ''',
        subtype='html'
    )
    return email