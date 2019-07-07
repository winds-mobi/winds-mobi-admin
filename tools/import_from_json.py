import json

from winds_mobi_jdc.models import Station, StationStatus


def get_status(status):
    if status == 0:
        return StationStatus.unactive
    elif status == 1:
        return StationStatus.active
    elif status == 2:
        return StationStatus.maintenance
    elif status == 3:
        return StationStatus.test
    elif status == 4:
        return StationStatus.waiting
    elif status == 5:
        return StationStatus.wintering
    elif status == 6:
        return StationStatus.moved


with open('jdc.json') as f:
    stations = json.load(f)

for station in stations:
    Station.objects.create(
        id=station['id'],
        short_name=station['shortname'],
        name=station['name'],
        description=station['raw_description'],
        status=get_status(station['status_id']).name,
        latitude=station['lat'],
        longitude=station['long'],
        altitude=station['altitude'],
        phone_number=station['phone_nr'] if station['phone_nr'] else ''
    )
