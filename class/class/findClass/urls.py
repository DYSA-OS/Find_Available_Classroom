from django.urls import path
from .views import map_view, check_room, get_room_details, create_room, edit_room, delete_lecture, get_lecture_details

urlpatterns = [
    path('map/', map_view, name='map_view'),
    path('check_room/', check_room, name='check_room'),
    path('get_room_details/', get_room_details, name='get_room_details'),
    path('create_room/', create_room, name='create_room'),
    path('edit_room/', edit_room, name='edit_room'),
    path('delete_lecture/', delete_lecture, name='delete_lecture'),
    path('get_lecture_details/', get_lecture_details, name='get_lecture_details'),
]
