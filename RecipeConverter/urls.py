from django.urls import include, path
from . import views

from django.conf import settings
from django.conf.urls.static import static

#https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/

urlpatterns = [
    path('recipe_converter', views.recipe_converter, name='recipe_converter'),
    path('saved_conversions', views.saved_conversions, name='saved_conversions'),
    ]
