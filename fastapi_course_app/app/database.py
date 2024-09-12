from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


if settings.MODE == 'TEST':
    DATABASE_URL = settings.test_db_url
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.db_url
    DATABASE_PARAMS = {}

engine = create_async_engine(url=DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass



