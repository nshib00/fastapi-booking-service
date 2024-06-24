from fastapi import APIRouter, Depends, Response

from app.users.schemas import UserAuthSchema
from app.users.service import UsersService
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException


auth_router = APIRouter(prefix='/auth', tags=['Аутентификация'])
users_router = APIRouter(prefix='/users', tags=['Пользователи'])


@auth_router.post('/register')
async def register_user(user_data: UserAuthSchema):
    existing_user = await UsersService.find_one_or_none(email=user_data.email)
    if existing_user is not None:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersService.add(email=user_data.email, hashed_password=hashed_password)


@auth_router.post('/login')
async def login_user(response: Response, user_data: UserAuthSchema):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if user is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token(data={'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return {'access_token': access_token}


@auth_router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')


@users_router.get('/me')
async def get_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
