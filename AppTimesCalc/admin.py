#https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#adminsite-objects

from django.contrib import admin
from .models import *

class MeatTypeAdmin(admin.ModelAdmin):
    list_display = ('MeatTypeName', 'PortionKGPerAdult', 'PortionKGPerChild')

class CookingLevelAdmin(admin.ModelAdmin):
    list_display = ('CookingLevelSort', 'CookingLevel')

class CookingInfoAdmin(admin.ModelAdmin):
    list_display = ('MeatType', 'CookingLevel', 'NotRecommended', 'BrowningMins', 'OvenTempC', 'InternalTempC',
                    'MinsPerKg', 'MinsFixed', 'BrowningTempC', 'RestTimeMins')

class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('UserId','PlanName', 'MeatType', 'CookingLevel')

admin.site.register(MeatType, MeatTypeAdmin)
admin.site.register(CookingLevel, CookingLevelAdmin)
admin.site.register(CookingInfo, CookingInfoAdmin)
admin.site.register(MealPlan, MealPlanAdmin)

