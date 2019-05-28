from django.urls import include, path
from . import views

#https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/

urlpatterns = [
    path('', views.Home, name = 'Home'),
    path('Calculator', views.Calculator, name='Calculator'),
    path('CalcResult', views.CalcResult, name='CalcResult'),
    path('MealPlanner', views.MealPlanner, name='MealPlanner'),
    path('accounts/', include('allauth.urls')),
]