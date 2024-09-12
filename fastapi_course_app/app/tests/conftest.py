from functools import wraps
import pytest
from sqlalchemy import text
from httpx import ASGITransport, AsyncClient
from unittest import mock

from app.database import async_session_maker, engine, Base
from app.config import settings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from app.bookings.models import Bookings


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def get_test_db_queries() -> list[str]:
        with open('fastapi_course_app/app/tests/test_data_db.sql', encoding='utf-8') as file:
            queries_text = file.read()
        return queries_text.split(';')
    
    db_queries = get_test_db_queries()
    joined_db_queries = [
        query.replace('\n', ' ') for query in db_queries if query
    ]
    async with async_session_maker() as session:
        for query in joined_db_queries:
            await session.execute(text(query.strip()))
        await session.commit()


mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()   


from app.main import app as fastapi_app


@pytest.fixture(scope='function')
async def cli():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url='http://test',
    ) as ac:
        yield ac


@pytest.fixture(scope='session')
async def authed_cli():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app),
        base_url='http://test',
    ) as ac:
        await ac.post(
            url='/auth/login',
            json={
                'email': 'fedor@moloko.ru',
                'password': 'tut_budet_hashed_password_1',
            }
        )  
        assert ac.cookies.get('booking_access_token') is not None
        yield ac     


@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session




