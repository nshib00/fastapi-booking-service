from datetime import date

from fastapi import Query
from pydantic import BaseModel


class HotelsSchema(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int


class HotelsSchemaWithRoomsLeft(HotelsSchema):
    rooms_left: int = Query(ge=0)


class HotelsSearchArgs:
    def __init__(
        self,
        date_from: date,
        date_to: date,
    ):
        self.date_from = date_from
        self.date_to = date_to
