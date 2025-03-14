from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.config import settings
from app.users.auth import authenticate_user
from app.users.auth import create_access_token
from app.users.dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        user = await authenticate_user(username, password)
        if user is not None:
            access_token = create_access_token(data={'sub': str(user.id)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        user = await get_current_user(token)
        if not user:
            return False

        return True
    

admin_auth_backend = AdminAuth(secret_key=settings.SECRET_KEY)