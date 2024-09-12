from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ('testuser@test.com', 'testtesttest', 200),
        ('testuser@test.com', 'testtesttest2', 409),
        ('abcde', 'alskasjl', 422),
        ('testuser2@test.com', '', 400),
        ('testuser2@test.com', 'vasya2', 200),
    ]
)
async def test_register_user(cli: AsyncClient, email: str, password: str, status_code: int):
    response = await cli.post(
        url='/auth/register',
        json={'email': email, 'password': password}
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    'email, password, status_code',
    [
        ('testuser@test.com', 'testtesttest', 200),
        ('wrong@user.com', 'alskajlsk', 401),
        ('testuser@test.com', '', 400),
        ('', 'testtesttest', 422),
        ('alala', 'testtesttest', 422),
    ]
)
async def test_login_user(cli: AsyncClient, email: str, password: str, status_code: int):
    response = await cli.post(
        url='/auth/login',
        json={'email': email, 'password': password}
    )
    assert response.status_code == status_code