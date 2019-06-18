from django.contrib import admin
from .models import *

# Register your models here.


class ConverterAdmin(admin.ModelAdmin):
    list_display = ('unit_source_name', 'unit_dest_name', 'unit_conversion')


class ConversionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')


admin.site.register(Converter, ConverterAdmin)
admin.site.register(Conversion, ConversionAdmin)


