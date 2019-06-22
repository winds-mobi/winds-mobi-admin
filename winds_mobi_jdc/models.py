from enum import Enum

from django.db import models
from django.utils.translation import ugettext_lazy as _


class StationStatus(Enum):
    unactive = 'Unactive'
    active = 'Active'
    maintenance = 'Maintenance'
    test = 'Test'
    waiting = 'Waiting'
    wintering = 'Wintering'
    moved = 'Moved'


class Station(models.Model):
    id = models.PositiveIntegerField(_('Id'), primary_key=True)
    short_name = models.CharField(_('Short name'), max_length=50)
    name = models.CharField(_('Name'), max_length=128)
    description = models.TextField(_('Description'), blank=True)
    status = models.CharField(_('Status'), max_length=32, choices=((e.name, e.value) for e in StationStatus),
                              default=StationStatus.active.name)
    latitude = models.FloatField(_('Latitude'))
    longitude = models.FloatField(_('Longitude'))
    altitude = models.IntegerField(_('Altitude'))
    phone_number = models.CharField(_('Phone number'), max_length=32, blank=True)

    def __str__(self):
        return f'{self.short_name} ({self.id})'
