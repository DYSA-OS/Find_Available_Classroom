from django import forms
from .models import Lecture, LectureSchedule, Building, Room

class LectureForm(forms.ModelForm):
    building = forms.ModelChoiceField(queryset=Building.objects.all(), label="Building")

    class Meta:
        model = Lecture
        fields = ['subject', 'professor', 'lecture_type']

class LectureScheduleForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = forms.ChoiceField(choices=DAYS_OF_WEEK, label="Day")
    room_number = forms.CharField(label="Room Number")
    start_time1 = forms.TimeField(label="Start Time")
    end_time1 = forms.TimeField(label="End Time")
    day2 = forms.ChoiceField(choices=DAYS_OF_WEEK, label="Day 2", required=False)
    start_time2 = forms.TimeField(label="Start Time 2", required=False)
    end_time2 = forms.TimeField(label="End Time 2", required=False)

    class Meta:
        model = LectureSchedule
        fields = ['day', 'start_time1', 'end_time1', 'day2', 'start_time2', 'end_time2']
