# Unit-тесты моделей

import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from bookings.models import Hotel, Room, Booking


@pytest.mark.django_db
def test_hotel_creation():
    hotel = Hotel.objects.create(name="Grand Hotel")
    assert hotel.name == "Grand Hotel"
    assert str(hotel) == "Grand Hotel"

@pytest.mark.django_db
def test_room_creation():
    hotel = Hotel.objects.create(name="Grand Hotel")
    room = Room.objects.create(
        description = "Luxury Suite",
        price_per_night = 150.00,
        hotel = hotel
    )
    assert room.hotel == hotel
    assert str(room) == f"Room {room.id}: Luxury Suite"


@pytest.mark.django_db
def test_booking_date_validation():
    hotel = Hotel.objects.create(name="Grand Hotel")
    room = Room.objects.create(
        description="Suite",
        price_per_night=200.00,
        hotel=hotel
    )

    # 1. Проверка корректных дат
    valid_booking = Booking.objects.create(
        room=room,
        start_date=date(2025, 1, 10),
        end_date=date(2025, 1, 15)
    )
    assert valid_booking.start_date < valid_booking.end_date

    # 2. Проверка НЕкорректных дат
    invalid_booking = Booking(
        room=room,
        start_date=date(2025, 1, 20),
        end_date=date(2025, 1, 15)
    )

    # Проверяем через full_clean()
    with pytest.raises(ValidationError) as excinfo:
        invalid_booking.full_clean()

    # Проверяем наличие ошибки (теперь без привязки к конкретному полю)
    assert 'Дата окончания должна быть позже даты начала' in str(excinfo.value)

    # Альтернативный вариант - проверка через save()
    with pytest.raises(ValidationError):
        invalid_booking.save()