from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from sqladmin import ModelView


class UsersAdmin(ModelView, model=Users):
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    column_list = [Users.id, Users.email, "bookings"]
    column_details_list = [Users.id, Users.email, "bookings"]
    column_searchable_list = [Users.email]


class BookingsAdmin(ModelView, model=Bookings):
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-bookmark"

    column_list = [c.name for c in Bookings.__table__.columns if not c.name.endswith("_id")] + [
        Bookings.user
    ]
    column_details_list = [
        c.name for c in Bookings.__table__.columns if not c.name.endswith("_id")
    ] + [Bookings.user]
    column_searchable_list = ["user.email", Bookings.date_from, Bookings.date_to]
    column_sortable_list = [
        Bookings.date_from,
        Bookings.date_to,
        Bookings.price,
        Bookings.total_days,
        Bookings.total_cost,
    ]


class HotelsAdmin(ModelView, model=Hotels):
    can_delete = False
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"

    column_list = [Hotels.id, Hotels.name, Hotels.location, Hotels.rooms_quantity]
    column_details_exclude_list = [Hotels.image_id]


class RoomsAdmin(ModelView, model=Rooms):
    can_delete = False
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-door-closed"

    column_list = [Rooms.id, Rooms.name, "hotel", Rooms.price, Rooms.quantity, "booking"]
    column_details_exclude_list = [Hotels.image_id]


ALL_ADMIN_VIEWS = (UsersAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin)
