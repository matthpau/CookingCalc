from django.contrib import admin
from .models import Store, StoreComment
from django.contrib.gis.admin import OSMGeoAdmin


@admin.register(Store)
class StoreAdmin(OSMGeoAdmin):
    list_display = ('id', 'name', 'location')
    readonly_fields = ['address_full', 'address_url']
admin.site.register(StoreComment)

