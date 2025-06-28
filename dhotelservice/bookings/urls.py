from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add/', views.add_room),
    path('delete/', views.delete_room),
    path('list/', views.list_rooms),
    path('add_booking/', views.add_booking),
    path('delete_booking/', views.delete_booking),
    path('list_bookings/', views.list_bookings_by_hotel),
]