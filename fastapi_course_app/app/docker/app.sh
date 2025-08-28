#!/bin/bash

alembic upgrade head
gunicorn fastapi_course_app.app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000