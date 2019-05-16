from django.urls import path
from . import views

#https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/

urlpatterns = [
    path('', views.Calculator, name='calculator'),
    path('User', views.UserPage, name='UserPage'),

]