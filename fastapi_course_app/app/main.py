from fastapi import FastAPI
import uvicorn

from bookings.router import router as bookings_router
from users.router import users_router, auth_router
from hotels.router import router as hotels_router
from hotels.rooms.router import router as rooms_router


app = FastAPI()
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=9000, reload=True)
