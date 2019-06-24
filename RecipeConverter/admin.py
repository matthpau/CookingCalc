from django.contrib import admin
from .models import *

# Register your models here.


class ConverterAdmin(admin.ModelAdmin):
    list_display = ('unit_source_name', 'unit_source_type', 'unit_source_keys', 'cup_type', 'spoon_type',
                    'unit_dest_name', 'unit_conversion')


class ConversionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(Converter, ConverterAdmin)
admin.site.register(Conversion, ConversionAdmin)


