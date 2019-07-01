from django.contrib import admin
from .models import Store, StoreComment
from django.contrib.gis.admin import OSMGeoAdmin


@admin.register(Store)
class StoreAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')


admin.site.register(StoreComment)

