# Фикстуры

import pytest
from django.test import Client

@pytest.fixture
def api_client():
    return Client()

@pytest.fixture
def sample_hotel():
    from ..models import Hotel
    return Hotel.objects.create(name="Test Hotel")

@pytest.fixture
def sample_room(sample_hotel):
    from ..models import Room
    return Room.objects.create(
        description="Test Room",
        price_per_night=100.00,
        hotel=sample_hotel
    )