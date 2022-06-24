from django.contrib import admin

from winds_mobi_zermatt.models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("id", "short_name", "name", "latitude", "longitude", "altitude")
