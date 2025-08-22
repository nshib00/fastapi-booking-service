import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location, date_from, date_to, status_code",
    [
        ("Алтай", "2023-07-20", "2023-08-04", 200),
        ("Коми", "2023-08-01", "2023-08-08", 200),
        ("Алтай", "2023-07-20", "2023-06-30", 400),
        ("Коми", "2023-07-20", "2023-09-01", 400),
    ],
)
async def test_get_hotels(
    cli: AsyncClient, location: str, date_from: str, date_to: str, status_code: int
):
    response = await cli.get(
        f"/hotels/{location}", params={"date_from": date_from, "date_to": date_to}
    )
    assert response.status_code == status_code
