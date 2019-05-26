#https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#adminsite-objects

from django.contrib import admin
from .models import *

class MeatTypeAdmin(admin.ModelAdmin):
    list_display = ('MeatTypeName', 'PortionKGPerAdult', 'PortionKGPerChild')

class CookingLevelAdmin(admin.ModelAdmin):
    list_display = ('CookingLevelSort', 'CookingLevel')

class CookingInfoAdmin(admin.ModelAdmin):
    list_display = ('MeatType', 'CookingLevel', 'NotRecommended', 'OvenTempC', 'InternalTempC',
                    'MinsPerKg', 'MinsFixed', 'InitialOvenTempC', 'InitialOvenTimeMins', 'RestTimeMins')

admin.site.register(MeatType, MeatTypeAdmin)
admin.site.register(CookingLevel, CookingLevelAdmin)
admin.site.register(CookingInfo, CookingInfoAdmin)
admin.site.register(CookingPlan)

