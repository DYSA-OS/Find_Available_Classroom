from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Room(models.Model):
    building = models.ForeignKey(Building, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.building.name} - {self.name}'

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
