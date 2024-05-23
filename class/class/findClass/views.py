from django.shortcuts import render
from .models import Lecture, Building, Room

def map_view(request):
    lectures = Lecture.objects.select_related('room__building').all()

    # geojson형식으로 map.html에 옮기기
    features = []
    for lecture in lectures:
        building = lecture.room.building
        feature = {
            'type': 'Feature',
            'properties': {
                'description': f'<strong>{lecture.subject}</strong><p><li>{lecture.professor}</li><li>{lecture.lecture_type}</li><li>{building.name}</li><li>{lecture.room.room_number}</li></p>'
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [building.longitude, building.latitude]
            }
        }
        features.append(feature)

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    context = {
        'geojson': geojson
    }

    return render(request, 'findClass/map.html', context)
