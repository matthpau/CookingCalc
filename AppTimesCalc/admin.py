#https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#adminsite-objects

from .models import *
from django.contrib import admin


class MeatTypeAdmin(admin.ModelAdmin):
    list_display = ('MeatTypeName', 'PortionKGPerAdult', 'PortionKGPerChild')


class CookingLevelAdmin(admin.ModelAdmin):
    list_display = ('CookingLevelSort', 'CookingLevel')


class CookingInfoAdmin(admin.ModelAdmin):
    list_display = ('MeatType', 'CookingLevel', 'NotRecommended', 'BrowningMins', 'OvenTempC', 'InternalTempC',
                    'MinsPerKg', 'MinsFixed', 'BrowningTempC', 'RestTimeMins')


class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'User', 'PlanName', 'MeatType', 'CookingLevel')
    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(MeatType, MeatTypeAdmin)
admin.site.register(CookingLevel, CookingLevelAdmin)
admin.site.register(CookingInfo, CookingInfoAdmin)
admin.site.register(MealPlan, MealPlanAdmin)

