from django.contrib import admin

from winds_mobi_jdc.models import Station


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'short_name', 'latitude', 'longitude', 'altitude', 'status')
    list_filter = ('status',)
