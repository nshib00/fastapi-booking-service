from datetime import datetime, timezone

import jwt
from app.config import settings
from app.exceptions import TokenAbsentException, TokenExpiredException, UserNotExistsException
from app.users.service import UsersService
from fastapi import Depends, Request


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if token is None:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except jwt.PyJWTError:
        raise TokenAbsentException
    expire: str | None = payload.get("exp")
    if expire is None or int(expire) < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise UserNotExistsException
    user = await UsersService.find_by_id(int(user_id))
    if user is None:
        raise UserNotExistsException
    return user
