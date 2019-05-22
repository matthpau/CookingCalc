from django.urls import path
from . import views

#https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/

urlpatterns = [
    path('', views.Calculator, name='Calculator'),
    path('calc-result', views.CalcResult, name='CalcResult'),
    path('MealPlanner', views.MealPlanner, name='MealPlanner'),
]