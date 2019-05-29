from django.urls import include, path
from . import views

#https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/

urlpatterns = [
    path('', views.Home, name = 'Home'),
    path('Calculator_w', views.Calculator_w, name='Calculator_w'),
    path('Calculator_p', views.Calculator_p, name='Calculator_p'),
    path('CalcResult', views.CalcResult, name='CalcResult'),
    path('MealPlanner', views.MealPlanner, name='MealPlanner'),
    path('accounts/', include('allauth.urls')),
    path('About', views.About, name='About'),
]