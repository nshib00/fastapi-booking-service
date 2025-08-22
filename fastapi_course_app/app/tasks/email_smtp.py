import smtplib
from email.message import EmailMessage

from app.config import settings


def send_email_via_smtp(email: EmailMessage) -> None:
    with smtplib.SMTP_SSL(
        host=settings.SMTP_HOST, port=settings.SMTP_PORT, timeout=10
    ) as smtp_server:
        smtp_server.login(user=settings.SMTP_USER, password=settings.SMTP_PASS)
        smtp_server.send_message(email)
