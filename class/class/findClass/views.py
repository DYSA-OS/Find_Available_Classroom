import json
from django.shortcuts import render
from .models import Building, Room, LectureSchedule
from datetime import datetime, time

def map_view(request):
    # 현재 시간을 임의로 수요일 오전 11시로 설정
    now = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
    current_day = 'Wednesday'
    current_time = time(now.hour, now.minute)

    # 강의실 정보를 저장할 리스트
    occupied_rooms = set()
    available_rooms = set()

    # 모든 강의실을 가져와서 초기화
    all_rooms = Room.objects.all()
    for room in all_rooms:
        available_rooms.add(room)

    # 현재 시간에 해당하는 스케줄을 가져와서 처리
    schedules = LectureSchedule.objects.select_related('lecture__room__building').filter(day=current_day)
    for schedule in schedules:
        if schedule.start_time <= current_time < schedule.end_time:
            occupied_rooms.add(schedule.lecture.room)
            if schedule.lecture.room in available_rooms:
                available_rooms.remove(schedule.lecture.room)

    # 강의실 정보를 빌딩별로 그룹화하여 GeoJSON 형식으로 변환
    features = []

    buildings = Building.objects.all()
    for building in buildings:
        building_rooms_occupied = [room.room_number for room in occupied_rooms if room.building == building]
        building_rooms_available = [room.room_number for room in available_rooms if room.building == building]

        features.append({
            'type': 'Feature',
            'properties': {
                'name': building.name,
                'occupied_count': len(building_rooms_occupied),
                'available_count': len(building_rooms_available),
                'occupied_rooms': building_rooms_occupied,
                'available_rooms': building_rooms_available,
                'description': f'<strong>{building.name}</strong><p><strong>Occupied Rooms:</strong> {len(building_rooms_occupied)}<br><strong>Available Rooms:</strong> {len(building_rooms_available)}</p>'
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [building.longitude, building.latitude]
            }
        })

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    context = {
        'geojson': json.dumps(geojson)
    }

    return render(request, 'findClass/map.html', context)
