import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Building, Room, LectureSchedule, Lecture
from datetime import datetime, time
from .forms import LectureForm, LectureScheduleForm  # 폼을 추가

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
                'id': schedule.lecture.id,  # 여기서 id를 포함시킵니다
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


def create_room(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        schedule_form = LectureScheduleForm(request.POST)
        if form.is_valid() and schedule_form.is_valid():
            building = form.cleaned_data['building']
            room_number = schedule_form.cleaned_data['room_number']
            room, created = Room.objects.get_or_create(building=building, room_number=room_number)
            lecture = form.save(commit=False)
            lecture.room = room
            lecture.save()

            schedule = LectureSchedule(
                lecture=lecture,
                day=schedule_form.cleaned_data['day'],
                start_time=schedule_form.cleaned_data['start_time1'],
                end_time=schedule_form.cleaned_data['end_time1']
            )
            schedule.save()

            day2 = schedule_form.cleaned_data.get('day2')
            start_time2 = schedule_form.cleaned_data.get('start_time2')
            end_time2 = schedule_form.cleaned_data.get('end_time2')

            if day2 and start_time2 and end_time2:
                LectureSchedule.objects.create(
                    lecture=lecture,
                    day=day2,
                    start_time=start_time2,
                    end_time=end_time2
                )

            return JsonResponse({'success': True, 'message': 'Lecture created successfully.'})
        else:
            errors = {**form.errors, **schedule_form.errors}
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def get_lecture_details(request):
    lecture_id = request.GET.get('id')
    lecture = get_object_or_404(Lecture, id=lecture_id)
    schedules = lecture.schedules.all()
    response_data = {
        'id': lecture.id,
        'subject': lecture.subject,
        'professor': lecture.professor,
        'lecture_type': lecture.lecture_type,
        'building_id': lecture.room.building.id,
        'room_number': lecture.room.room_number,
        'day': schedules[0].day,
        'start_time1': schedules[0].start_time,
        'end_time1': schedules[0].end_time,
    }
    if len(schedules) > 1:
        response_data.update({
            'day2': schedules[1].day,
            'start_time2': schedules[1].start_time,
            'end_time2': schedules[1].end_time,
        })
    return JsonResponse(response_data)


def edit_room(request):
    if request.method == 'POST':
        lecture_id = request.POST.get('lecture_id')
        lecture = get_object_or_404(Lecture, id=lecture_id)

        lecture_form = LectureForm(request.POST, instance=lecture)
        schedule_form = LectureScheduleForm(request.POST)

        if lecture_form.is_valid() and schedule_form.is_valid():
            lecture_form.save()

            room_number = schedule_form.cleaned_data['room_number']
            day = schedule_form.cleaned_data['day']
            start_time1 = schedule_form.cleaned_data['start_time1']
            end_time1 = schedule_form.cleaned_data['end_time1']

            LectureSchedule.objects.filter(lecture=lecture).delete()
            LectureSchedule.objects.create(lecture=lecture, day=day, start_time=start_time1, end_time=end_time1)

            day2 = schedule_form.cleaned_data.get('day2')
            start_time2 = schedule_form.cleaned_data.get('start_time2')
            end_time2 = schedule_form.cleaned_data.get('end_time2')

            if day2 and start_time2 and end_time2:
                LectureSchedule.objects.create(lecture=lecture, day=day2, start_time=start_time2, end_time=end_time2)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': {**lecture_form.errors, **schedule_form.errors}})

    return JsonResponse({'success': False, 'errors': 'Invalid request'})


@csrf_exempt  # CSRF 검사 비활성화
def delete_lecture(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lecture_id = data.get('id')
            if not lecture_id:
                return JsonResponse({'success': False, 'error': 'No lecture ID provided'}, status=400)

            lecture = get_object_or_404(Lecture, id=lecture_id)
            lecture.delete()
            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)