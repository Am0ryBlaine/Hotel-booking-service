from django.db import models
from datetime import date

class Hotel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Room(models.Model):
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return f'Room {self.id}: {self.description}'


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Booking {self.id} for Room {self.room.id} from {self.start_date} to {self.end_date}'
