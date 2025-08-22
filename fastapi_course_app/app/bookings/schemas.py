from datetime import date

from pydantic import BaseModel


class BookingsSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int


class BookingsResponseSchema(BookingsSchema):
    image_id: int
    name: str
    description: str
    services: list[str]
