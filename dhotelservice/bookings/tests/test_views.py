# Интеграционные тесты API

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from bookings.models import Hotel, Room, Booking
import json

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_hotel():
    return Hotel.objects.create(name="Test Hotel")

@pytest.fixture
def sample_room(sample_hotel):
    return Room.objects.create(
        description="Test room",
        price_per_night=100.00,
        hotel=sample_hotel
    )

@pytest.mark.django_db
def test_add_room(api_client, sample_hotel):
    url = reverse("add_room")
    data = {
        "description": "Deluxe Room",
        "price_per_night": 200.00,
        "hotel_id": sample_hotel.id
    }
    response = api_client.post(
        url,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.django_db
def test_add_booking(api_client, sample_room):
    url = reverse("add_booking")
    data = {
        "room_id": sample_room.id,
        "start_date": "10.01.2025",
        "end_date": "15.01.2025",
    }
    response = api_client.post(
        url,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert Booking.objects.count() == 1

@pytest.mark.django_db
def test_add_booking_invalid_dates(api_client, sample_room):
    url = reverse("add_booking")
    data = {
        "room_id": sample_room.id,
        "start_date": "20.01.2025",  # Дата начала > даты окончания
        "end_date": "15.01.2025"
    }
    response = api_client.post(
        url,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert "Дата начала позже даты окончания" in response.json()["Ошибка"]

@pytest.mark.django_db
def test_delete_room(api_client, sample_room):
    url = reverse("delete_room")
    data = {
        "id": sample_room.id
    }
    response = api_client.delete(
        url,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert "Статус" in response.json()
    assert Room.objects.count() == 0

@pytest.mark.django_db
def test_list_rooms(api_client, sample_room):
    url = reverse("list_rooms")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["Номер"] == sample_room.id