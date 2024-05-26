from findClass.models import Lecture, LectureSchedule
from django.db.models import Min, Max

# 모든 강의를 가져와서 처리
lectures = Lecture.objects.all()
for lecture in lectures:
    # 해당 강의의 모든 스케줄을 가져옴
    schedules = LectureSchedule.objects.filter(lecture=lecture)

    # 강의 스케줄을 요일별로 그룹화
    grouped_schedules = schedules.values('day').annotate(
        start_time=Min('start_time'),
        end_time=Max('end_time')
    )

    # 기존 스케줄 삭제
    schedules.delete()

    # 그룹화된 스케줄을 새로운 스케줄로 저장
    for schedule in grouped_schedules:
        LectureSchedule.objects.create(
            lecture=lecture,
            day=schedule['day'],
            start_time=schedule['start_time'],
            end_time=schedule['end_time']
        )
