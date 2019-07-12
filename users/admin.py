from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile, Country


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'email', 'username', ]

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['id', 'user']
    readonly_fields = ['auto_address']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Country)
