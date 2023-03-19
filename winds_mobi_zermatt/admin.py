from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from winds_mobi_zermatt.models import Station


@admin.register(Station)
class StationAdmin(ImportExportModelAdmin):
    ordering = ("id",)
    list_display = ("id", "short_name", "name", "latitude", "longitude", "altitude")
