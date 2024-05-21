from django.contrib import admin
from .models import Building, Room, Lecture, LectureSchedule

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Lecture)
admin.site.register(LectureSchedule)
