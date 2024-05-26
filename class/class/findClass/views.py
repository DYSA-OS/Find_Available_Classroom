import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Building, Room, LectureSchedule
from datetime import datetime, time

def map_view(request):
    datetime_str = request.GET.get('datetime')
    if datetime_str:
        now = datetime.fromisoformat(datetime_str)
    else:
        # 현재 시간을 임의로 수요일 오전 11시로 설정
        now = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
    current_day = now.strftime('%A')
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
        'geojson': json.dumps(geojson),
        'buildings': buildings  # 건물 목록을 컨텍스트에 추가
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(geojson)

    return render(request, 'findClass/map.html', context)

def get_room_details(request):
    datetime_str = request.GET.get('datetime')
    building_name = request.GET.get('building_name')
    room_number = request.GET.get('room_number')
    if not datetime_str or not building_name or not room_number:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    now = datetime.fromisoformat(datetime_str)
    current_day = now.strftime('%A')
    current_time = time(now.hour, now.minute)

    building = get_object_or_404(Building, name=building_name)
    room = get_object_or_404(Room, building=building, room_number=room_number)

    schedules = LectureSchedule.objects.filter(
        lecture__room=room,
        day=current_day,
        start_time__lte=current_time,
        end_time__gt=current_time
    )

    if schedules.exists():
        lectures = [
            {
                'subject': schedule.lecture.subject,
                'professor': schedule.lecture.professor,
                'lecture_type': schedule.lecture.lecture_type,
                'day': schedule.day,
                'start_time': schedule.start_time.strftime('%H:%M'),
                'end_time': schedule.end_time.strftime('%H:%M')
            }
            for schedule in schedules
        ]
        return JsonResponse({'available': False, 'lectures': lectures})
    else:
        return JsonResponse({'available': True})

def check_room(request):
    datetime_str = request.GET.get('datetime')
    building_name = request.GET.get('building_name')
    room_number = request.GET.get('room_number')
    if not datetime_str or not building_name or not room_number:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    now = datetime.fromisoformat(datetime_str)
    current_day = now.strftime('%A')
    current_time = time(now.hour, now.minute)

    building = get_object_or_404(Building, name=building_name)
    room = get_object_or_404(Room, building=building, room_number=room_number)

    schedules = LectureSchedule.objects.filter(
        lecture__room=room,
        day=current_day,
        start_time__lte=current_time,
        end_time__gt=current_time
    )

    if schedules.exists():
        lectures = [
            {
                'subject': schedule.lecture.subject,
                'professor': schedule.lecture.professor,
                'lecture_type': schedule.lecture.lecture_type,
                'day': schedule.day,
                'start_time': schedule.start_time.strftime('%H:%M'),
                'end_time': schedule.end_time.strftime('%H:%M')
            }
            for schedule in schedules
        ]
        return JsonResponse({'available': False, 'lectures': lectures})
    else:
        return JsonResponse({'available': True})
