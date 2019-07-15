from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('<int:store_id>/profile', views.store_profile, name='store_profile'),
    path('like', views.store_like, name='store_like'),
    path('search', views.store_search, name='store_search'),
    path('get_loc', views.get_loc, name='get_loc'),
    path('process_loc', views.process_loc, name='process_loc'),
    path('<int:store_id>/eventslist', views.EventsList.as_view(), name='eventslist'),
    path('<int:store_id>/create_event', views.CreateEvent.as_view(), name='create_event'),
    path('<int:event_id>/update_event', views.UpdateEvent.as_view(), name='update_event'),
    path('<int:event_id>/delete_event', views.DeleteEvent.as_view(), name='delete_event')
    ]
