from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_room, name='add_room'),
    path('delete/', views.delete_room, name='delete_room'),
    path('list/', views.list_rooms, name='list_rooms'),
    path('add_booking/', views.add_booking, name='add_booking'),
    path('delete_booking/', views.delete_booking, name='delete_booking'),
    path('list_bookings/', views.list_bookings_by_hotel, name='list_bookings'),
]