from django.contrib import admin
from .models import Store, StoreComment
from django.contrib.gis.admin import OSMGeoAdmin


@admin.register(Store)
class StoreAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
    readonly_fields = ['addr_full', 'url_search']

admin.site.register(StoreComment)

