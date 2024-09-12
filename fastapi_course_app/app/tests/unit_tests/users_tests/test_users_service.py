import pytest

from app.users.service import UsersService


@pytest.mark.parametrize(
    'id, email, user_exists',
    [
        (1, 'fedor@moloko.ru', True),
        (2, 'sharik@moloko.ru', True),
        (10, 'nonexisting@user.com', False)
    ]
)
async def test_find_user_by_id(id: int, email: str, user_exists: bool):
    user = await UsersService.find_by_id(id)
    if user_exists:
        assert user is not None
        assert user.id == id
        assert user.email == email
    else:
        assert user is None


# async def test_find_user_me():
#     pass