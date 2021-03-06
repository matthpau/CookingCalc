from django.urls import path
from . import views

#https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/

app_name = 'converter'
urlpatterns = [
    path('recipe_converter', views.recipe_converter, name='recipe_converter'),
    path('saved_conversions', views.ConversionsList.as_view(), name='saved_conversions'),
    path('converter_about', views.converter_about, name='ConverterAbout'),
    path('<int:pk>/update', views.ConversionUpdate.as_view(), name='ConversionUpdate'),
    path('<int:pk>/delete', views.ConversionDelete, name='ConversionDelete')
    ]
