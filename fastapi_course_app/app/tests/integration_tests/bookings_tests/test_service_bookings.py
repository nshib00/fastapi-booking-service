from datetime import datetime

from app.bookings.service import BookingsService


async def test_booking_service():
    date_from = datetime.strptime("2025-01-01", "%Y-%m-%d")
    date_to = datetime.strptime("2025-01-14", "%Y-%m-%d")

    booking_id = await BookingsService.add(
        user_id=1,
        room_id=1,
        date_from=date_from,
        date_to=date_to,
    )
    new_booking = await BookingsService.find_by_id(booking_id)
    assert new_booking is not None

    await BookingsService.delete(model_id=booking_id)
    new_booking_after_deletion = await BookingsService.find_by_id(booking_id)
    assert new_booking_after_deletion is None
