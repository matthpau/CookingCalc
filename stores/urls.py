from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('<int:store_id>/profile', views.store_profile, name='store_profile'),
    path('like', views.store_like, name='store_like'),
    path('search', views.store_search, name='store_search'),
    path('get_loc', views.get_loc, name='get_loc'),
    path('process_loc', views.process_loc, name='process_loc')
    ]
