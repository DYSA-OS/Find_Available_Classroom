import os
import django
from django.db.models import Min, Max

# Django settings 모듈 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'class.settings')
django.setup()

from findClass.models import Lecture, LectureSchedule

def remove_duplicate_schedules():
    # Step 1: 병합된 스케줄을 새로 생성
    lectures = Lecture.objects.all()
    for lecture in lectures:
        # 해당 강의의 모든 스케줄을 가져옴
        schedules = LectureSchedule.objects.filter(lecture=lecture)

        # 강의 스케줄을 요일별로 그룹화
        grouped_schedules = schedules.values('day').annotate(
            start_time=Min('start_time'),
            end_time=Max('end_time')
        )

        # 그룹화된 스케줄을 새로운 스케줄로 저장
        for schedule in grouped_schedules:
            LectureSchedule.objects.create(
                lecture=lecture,
                day=schedule['day'],
                start_time=schedule['start_time'],
                end_time=schedule['end_time']
            )

    # Step 2: 중복된 스케줄 삭제
    with django.db.connection.cursor() as cursor:
        cursor.execute("""
            DELETE ls1 FROM findClass_lectureschedule ls1
            INNER JOIN findClass_lectureschedule ls2 
            WHERE 
                ls1.id > ls2.id AND 
                ls1.lecture_id = ls2.lecture_id AND 
                ls1.day = ls2.day AND 
                ls1.start_time = ls2.start_time AND 
                ls1.end_time = ls2.end_time;
        """)

if __name__ == '__main__':
    remove_duplicate_schedules()
