from typing import Type

from app.database import async_session_maker
from sqlalchemy import (
    DeclarativeBase,
    Delete,
    Insert,
    MappingResult,
    Update,
    delete,
    insert,
    select,
    update,
)


class BaseService:
    model: Type[DeclarativeBase] | None = None

    @classmethod
    async def __get_result_query(cls, **filters) -> MappingResult:
        if cls.model is None:
            raise ValueError("Model is not defined")
        query = select(cls.model.__table__.columns).filter_by(**filters)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings()

    @classmethod
    async def __execute_query_with_commit(cls, query: Insert | Update | Delete):
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_all(cls, **filters):
        result = await cls.__get_result_query(**filters)
        return result.all()

    @classmethod
    async def find_one_or_none(cls, **filters):
        result = await cls.__get_result_query(**filters)
        return result.one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int):
        result = await cls.__get_result_query(id=model_id)
        return result.one_or_none()

    @classmethod
    async def add(cls, **data):
        if cls.model is None:
            raise ValueError("Model is not defined")
        query = insert(cls.model).values(**data)
        await cls.__execute_query_with_commit(query)

    @classmethod
    async def update(cls, model_id: int, **data):
        if cls.model is None:
            raise ValueError("Model is not defined")
        query = update(cls.model).where(cls.model.id == model_id).values(**data)
        await cls.__execute_query_with_commit(query)

    @classmethod
    async def delete(cls, model_id: int):
        if cls.model is None:
            raise ValueError("Model is not defined")
        query = delete(cls.model).where(cls.model.id == model_id)
        await cls.__execute_query_with_commit(query)
