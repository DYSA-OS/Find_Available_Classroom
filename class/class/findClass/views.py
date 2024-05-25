import json
import logging
from django.http import JsonResponse
from django.shortcuts import render
from .models import Building, Room, Lecture, LectureSchedule
from datetime import datetime, time

logger = logging.getLogger(__name__)

def map_view(request):
    # 현재 시간을 임의로 수요일 오전 11시로 설정
    now = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
    current_day = 'Wednesday'
    current_time = time(now.hour, now.minute)

    # 사용 중인 강의실과 사용 가능한 강의실을 구분
    occupied_rooms = []
    available_rooms = []

    schedules = LectureSchedule.objects.select_related('lecture__room__building').filter(day=current_day)

    for schedule in schedules:
        if schedule.start_time <= current_time < schedule.end_time:
            occupied_rooms.append(schedule.lecture.room)
        else:
            available_rooms.append(schedule.lecture.room)

    # 중복 제거
    occupied_rooms = list(set(occupied_rooms))
    available_rooms = list(set(available_rooms))

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

    # Log the GeoJSON data
    logger.info(json.dumps(geojson, indent=2))

    context = {
        'geojson': json.dumps(geojson)
    }

    return render(request, 'findClass/map.html', context)

def get_room_details(request):
    room_number = request.GET.get('room_number')
    logger.info(f"Received request for room number: {room_number}")  # 로그 추가
    try:
        room = Room.objects.get(room_number=room_number)
        lectures = room.lectures.all()
        lecture_details = []
        for lecture in lectures:
            schedules = lecture.schedules.all()
            for schedule in schedules:
                lecture_details.append({
                    'subject': lecture.subject,
                    'professor': lecture.professor,
                    'lecture_type': lecture.lecture_type,
                    'day': schedule.day,
                    'start_time': schedule.start_time.strftime('%H:%M'),
                    'end_time': schedule.end_time.strftime('%H:%M')
                })
        logger.info(f"Lecture details for room {room_number}: {lecture_details}")  # 로그 추가
        return JsonResponse({'lectures': lecture_details})
    except Room.DoesNotExist:
        logger.error(f"Room not found: {room_number}")  # 로그 추가
        return JsonResponse({'error': 'Room not found'}, status=404)
