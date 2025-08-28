FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock* ./

RUN pip3 install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY fastapi_course_app/app/docker/*.sh /app/docker/

COPY . .

RUN chmod +x /app/docker/*.sh
