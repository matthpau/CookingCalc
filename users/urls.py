from django.urls import include, path
from . import views

app_name = 'users'
urlpatterns = [
    path('profile', views.update_profile, name='profile'),
    path('check_address', views.check_address, name='check_address'),
    path('<int:user_id>/delete', views.UserDelete.as_view(), name='delete')
    ]
