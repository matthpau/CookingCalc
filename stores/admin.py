from django.contrib import admin
from django import forms
from django.contrib.gis.db import models
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Store, StoreComment, Country, StoreType, Event, AuthorisedEventEditors


@admin.register(Store)
class StoreAdmin(OSMGeoAdmin):
    list_display = ('id', 'name', 'my_address', 'my_country')
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['name'] 

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['store']

class AuthorisedEventEditorsAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['store']

class StoreTypeAdmin(admin.ModelAdmin):
    list_display = ['type_text', 'icon_text']

admin.site.register(StoreComment)
admin.site.register(Country)
admin.site.register(StoreType, StoreTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(AuthorisedEventEditors, AuthorisedEventEditorsAdmin)
