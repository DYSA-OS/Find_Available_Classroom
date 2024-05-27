from django.urls import path
from .views import map_view, check_room, get_room_details, create_room

urlpatterns = [
    path('map/', map_view, name='map_view'),
    path('get_room_details/', get_room_details, name='get_room_details'),
    path('check_room/', check_room, name='check_room'),
    path('create_room/', create_room, name='create_room'),
]
