from django.urls import include, path
from . import views

app_name = 'users'
urlpatterns = [
    path('profile', views.update_profile, name='profile')
    ]