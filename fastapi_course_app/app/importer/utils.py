import json
from datetime import datetime


def normalize_row(row: dict) -> dict:
    FIELDS_TO_NORMALIZE_TO_INT = (
        'rooms_quantity', 'image_id',  # hotels
        'hotel_id', 'price', 'quantity',  # rooms
        'room_id', 'user_id',  # bookings
    )

    for field in FIELDS_TO_NORMALIZE_TO_INT:
        if row.get(field) is not None:
            row[field] = int(row[field])

    services = row.get('services')
    if services is not None:
        row['services'] = json.loads(row['services']) if services else []

    if row.get('date_from') is not None and row.get('date_to') is not None:
        row['date_from'] = datetime.strptime(row['date_from'].replace('`', ''), "%Y-%m-%d").date()
        row['date_to'] = datetime.strptime(row['date_to'].replace('`', ''), "%Y-%m-%d").date()

    return row
