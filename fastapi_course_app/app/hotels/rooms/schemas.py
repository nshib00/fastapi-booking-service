from datetime import date
from pydantic import BaseModel


class RoomsSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int


class RoomsSearchArgs:
    def __init__(self, date_from: date, date_to: date, price: int | None = None, filter_operator: str = '='):
        self.date_from = date_from
        self.date_to = date_to
        self.price = price
        self.filter_operator = filter_operator
        