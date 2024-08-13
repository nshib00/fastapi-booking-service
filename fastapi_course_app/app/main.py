from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import uvicorn

from bookings.router import router as bookings_router
from users.router import users_router, auth_router
from hotels.router import router as hotels_router
from hotels.rooms.router import router as rooms_router

from pages.router import router as pages_router
from images.router import router as images_router

from config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis_client = aioredis.from_url(settings.REDIS_URL, encoding='utf-8', decode_responses=True)
    FastAPICache.init(backend=RedisBackend(redis_client), prefix='fastapi-cache')
    yield


app = FastAPI(lifespan=lifespan)
app.mount(path='/static', app=StaticFiles(directory='fastapi_course_app/app/static'), name='static')


all_routers = (users_router, bookings_router, auth_router, hotels_router, rooms_router, pages_router, images_router)
for router in all_routers:
    app.include_router(router)



if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=9000, reload=True)
