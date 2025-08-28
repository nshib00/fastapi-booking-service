# Booking service

Pet-проект - API для бронирования отелей.

## Запуск проекта

>Для запуска необходимо в корне проекта создать файл `.env.prod`. 
>
> Его можно создать на основе шаблона:
```ini
MODE=PROD
LOG_LEVEL=INFO

DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

TEST_DB_HOST=
TEST_DB_PORT=
TEST_DB_USER=
TEST_DB_PASS=
TEST_DB_NAME=

SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASS=

SECRET_KEY=
ALGORITHM=

REDIS_URL=

SENTRY_DSN=
```

Скачивание проекта, сборка и запуск:
```
git clone https://github.com/nshib00/fastapi-booking-service.git
cd fastapi-booking-service
docker compose up -d --build
```