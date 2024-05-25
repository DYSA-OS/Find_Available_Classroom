from django.urls import path
from .views import map_view, get_room_details

urlpatterns = [
    path('map/', map_view, name='map_view'),
    path('map/get_room_details/', get_room_details, name='get_room_details'),
]
