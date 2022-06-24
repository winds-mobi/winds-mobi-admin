from django.db import models
from django.utils.translation import gettext_lazy as _


class Station(models.Model):
    id = models.CharField(_('Id'), max_length=50, primary_key=True)
    short_name = models.CharField(_('Short name'), max_length=20)
    name = models.CharField(_('Name'), max_length=40)
    latitude = models.FloatField(_('Latitude'))
    longitude = models.FloatField(_('Longitude'))
    altitude = models.IntegerField(_('Altitude'), null=True, blank=True)

    def __str__(self):
        return f'{self.short_name} ({self.id})'
