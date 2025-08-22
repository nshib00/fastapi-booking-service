import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

app_path = Path(__file__).parent.parent
sys.path.insert(0, str(app_path))


from app.admin.auth import admin_auth_backend
from app.admin.views import ALL_ADMIN_VIEWS
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as rooms_router
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.pages.router import router as pages_router
from app.users.router import auth_router, users_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis_client = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    FastAPICache.init(backend=RedisBackend(redis_client), prefix="fastapi-cache")
    yield


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
    traces_sample_rate=1.0,
)

app = FastAPI(lifespan=lifespan)
app.mount(path="/static", app=StaticFiles(directory="fastapi_course_app/app/static"), name="static")


ALL_ROUTERS = (
    users_router,
    bookings_router,
    auth_router,
    hotels_router,
    rooms_router,
    pages_router,
    images_router,
)
for router in ALL_ROUTERS:
    app.include_router(router)


admin = Admin(app, engine, authentication_backend=admin_auth_backend)
for admin_view in ALL_ADMIN_VIEWS:
    admin.add_view(admin_view)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)
