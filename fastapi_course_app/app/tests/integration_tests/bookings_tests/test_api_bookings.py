from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    'room_id, date_from, date_to, booked_rooms, status_code',
    [
        *[(2, '2028-10-01', '2028-10-15', 2+i, 200) for i in range(10)],
        *[(2, '2028-10-01', '2028-10-15', 11, 409)] * 3,
        (1, '2028-10-01', '2028-09-01', 11, 400),
    ]
)
async def test_add_and_get_booking(
    authed_cli: AsyncClient, room_id: int, date_from: str, date_to: str, booked_rooms, status_code: int
):
    response = await authed_cli.post(
        '/bookings',
        params={
            'room_id': room_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    )   
    assert response.status_code == status_code

    bookings_response = await authed_cli.get('/bookings')
    assert len(bookings_response.json()) == booked_rooms


async def test_get_and_delete_booking(authed_cli: AsyncClient):
    bookings = await authed_cli.get('/bookings')
    bookings_json = bookings.json()
    booking_id = bookings_json[0].get('id')

    assert len(bookings_json) == 1
    assert booking_id == 1
    assert bookings_json[0].get('user_id') == 1

    await authed_cli.delete(f'/bookings/{booking_id}')
    bookings_after_deletion = await authed_cli.get('/bookings')
    assert not bookings_after_deletion.json()

