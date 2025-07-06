from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from winds_mobi_wunderground.models import Station


@admin.register(Station)
class StationAdmin(ImportExportModelAdmin):
    ordering = ("id",)
    list_display = ("id", "get_url")

    def get_url(self, obj):
        return mark_safe(
            f'<a href="https://www.wunderground.com/dashboard/pws/{obj.id}" target="_blank">Weather Underground</a>'
        )

    get_url.short_description = "WUnderground url"
