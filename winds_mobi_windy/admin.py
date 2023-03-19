from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from winds_mobi_windy.models import Station


@admin.register(Station)
class StationAdmin(ImportExportModelAdmin):
    ordering = ("id",)
    list_display = ("id",)
