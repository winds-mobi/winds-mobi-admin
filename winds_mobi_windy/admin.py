from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from winds_mobi_windy.models import Station


@admin.register(Station)
class StationAdmin(ImportExportModelAdmin):
    ordering = ("id",)
    list_display = ("id", "get_url")

    def get_url(self, obj):
        return mark_safe(f'<a href="https://www.windy.com/station/{obj.id}" target="_blank">Windy</a>')

    get_url.short_description = "Windy url"
