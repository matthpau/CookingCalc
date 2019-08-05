from django.urls import include, path
from . import views

app_name = 'users'
urlpatterns = [
    path('profile', views.update_profile, name='profile'),
    path('check_address', views.check_address, name='check_address'),
    path('delete_confirm', views.delete_confirm, name='delete_confirm'),
    path('delete', views.delete, name='delete'),
    ]
