from django.contrib import admin

from winds_mobi_windy.models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    ordering = ("id",)
    list_display = ("id",)
