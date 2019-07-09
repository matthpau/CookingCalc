from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Store, StoreComment, Country



@admin.register(Store)
class StoreAdmin(OSMGeoAdmin):
    list_display = ('id', 'name', 'my_address')
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(StoreComment)
admin.site.register(Country)
