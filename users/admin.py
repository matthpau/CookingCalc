from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile, Country


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    """
    I thought I was being clever here but this doesn't work cause the form doesnt save the store in order to select the user first
    #but there was a nice query there so I'll save it...
    e = Events.objects.first()
    my_queryset = CustomUser.objects.filter(authorisedeventeditors__store__event=e)
    """
    #form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'email', 'username', ]

@admin.register(Profile)
class ProfileAdmin(OSMGeoAdmin):
    model = Profile
    list_display = ['id', 'user']
    readonly_fields = ['auto_address']

admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(Profile, ProfileAdmin)
admin.site.register(Country)
