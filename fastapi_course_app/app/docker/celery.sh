#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery -A fastapi_course_app.app.tasks.celery:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery -A fastapi_course_app.app.tasks.celery:celery flower
elif [[ "${1}" == "beat" ]]; then
    celery -A fastapi_course_app.app.tasks.celery:celery beat -l INFO
fi