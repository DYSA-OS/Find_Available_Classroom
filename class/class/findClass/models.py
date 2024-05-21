from django.db import models
from django.utils import timezone

class Building(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Room(models.Model):
    building = models.ForeignKey(Building, related_name='rooms', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.building.name} - {self.room_number}'

    def get_capacity(self, day, start_time, end_time):
        lectures = self.lectures.filter(
            schedules__day=day,
            schedules__start_time__lt=end_time,
            schedules__end_time__gt=start_time
        )
        if lectures.exists():
            return 0  # 강의실이 사용 중인 경우 용량은 0
        else:
            return 50  # 예시로 빈 강의실의 기본 용량을 50으로 설정

class Lecture(models.Model):
    subject = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    lecture_type = models.CharField(max_length=50)
    room = models.ForeignKey(Room, related_name='lectures', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.subject} by {self.professor}'

class LectureSchedule(models.Model):
    lecture = models.ForeignKey(Lecture, related_name='schedules', on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.lecture.subject} on {self.day} from {self.start_time} to {self.end_time}'
