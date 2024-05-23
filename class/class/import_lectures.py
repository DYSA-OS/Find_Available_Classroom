import pandas as pd
from datetime import time
import os
import django


# Django settings 모듈 설정 (your_project_name은 실제 프로젝트 이름으로 변경)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'class.settings')
django.setup()

from findClass.models import Building, Room, Lecture, LectureSchedule



# 요일과 시간 정보 매핑
day_mapping = {
    '월': 'Monday',
    '화': 'Tuesday',
    '수': 'Wednesday',
    '목': 'Thursday',
    '금': 'Friday',
    '토': 'Saturday',
    '일': 'Sunday'
}


# 시간 블록을 파싱하여 시작 시간과 종료 시간을 반환하는 함수
def parse_time_block(block):
    time_blocks = {
        '0-A': (time(8, 0), time(8, 30)),
        '0-B': (time(8, 30), time(9, 0)),
        '1-A': (time(9, 0), time(9, 30)),
        '1-B': (time(9, 30), time(10, 0)),
        '2-A': (time(10, 0), time(10, 30)),
        '2-B': (time(10, 30), time(11, 0)),
        '3-A': (time(11, 0), time(11, 30)),
        '3-B': (time(11, 30), time(12, 0)),
        '4-A': (time(12, 0), time(12, 30)),
        '4-B': (time(12, 30), time(13, 0)),
        '5-A': (time(13, 0), time(13, 30)),
        '5-B': (time(13, 30), time(14, 0)),
        '6-A': (time(14, 0), time(14, 30)),
        '6-B': (time(14, 30), time(15, 0)),
        '7-A': (time(15, 0), time(15, 30)),
        '7-B': (time(15, 30), time(16, 0)),
        '8-A': (time(16, 0), time(16, 30)),
        '8-B': (time(16, 30), time(17, 0)),
        '9-A': (time(17, 0), time(17, 30)),
        '9-B': (time(17, 30), time(18, 0)),
        '10-A': (time(18, 0), time(18, 30)),
        '10-B': (time(18, 30), time(19, 0)),
        '11-A': (time(19, 0), time(19, 30)),
        '11-B': (time(19, 30), time(20, 0)),
        '12-A': (time(20, 0), time(20, 30)),
        '12-B': (time(20, 30), time(21, 0)),
        '13-A': (time(21, 0), time(21, 30)),
        '13-B': (time(21, 30), time(22, 0)),
        '14-A': (time(22, 0), time(22, 30)),
        '14-B': (time(22, 30), time(23, 0)),
    }
    return time_blocks[block]


# 주어진 시간 문자열을 파싱하여 요일, 시작 시간, 종료 시간 리스트를 반환하는 함수
def parse_times(time_str):
    time_entries = time_str.split(',')
    parsed_times = []

    for entry in time_entries:
        day_kor, block = entry.split()
        day_eng = day_mapping[day_kor]
        start_time, end_time = parse_time_block(block)
        parsed_times.append((day_eng, start_time, end_time))

    return parsed_times


def import_lectures():
    # 예시 데이터프레임 (여기서는 파일에서 읽어옵니다)
    df3 = pd.read_csv('findClass/df4.csv')

    # 데이터베이스에 저장
    for index, row in df3.iterrows():
        # Building 인스턴스를 가져오거나 생성
        building, created = Building.objects.get_or_create(
            name=row['building'],
            defaults={'latitude': row['latitude'], 'longitude': row['longitude']}
        )

        # Room 인스턴스를 가져오거나 생성
        room, created = Room.objects.get_or_create(
            building=building,
            room_number=row['building_room_number']
        )

        # Lecture 인스턴스를 생성
        lecture = Lecture.objects.create(
            subject=row['subject'],
            professor=row['professor'],
            lecture_type=row['lecture_type'],
            room=room
        )

        # LectureSchedule 인스턴스를 생성
        times = parse_times(row['time'])
        for day, start_time, end_time in times:
            LectureSchedule.objects.create(
                lecture=lecture,
                day=day,
                start_time=start_time,
                end_time=end_time
            )



if __name__ == '__main__':
    import_lectures()
