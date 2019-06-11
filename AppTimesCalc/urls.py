from django.urls import include, path
from . import views

#https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/

urlpatterns = [
    path('', views.Home, name='Home'),
    path('Calculator_w', views.Calculator_w, name='Calculator_w'),
    path('Calculator_p', views.Calculator_p, name='Calculator_p'),
    path('MealPlannerSaved', views.MealPlannerSaved, name='MealPlannerSaved'),
    path('MealPlanList', views.MealPlanList.as_view(), name='MealPlanList'),
    path('MealPlan/<int:pk>/update', views.MealPlanUpdate.as_view(), name='MealPlanUpdate'),
    path('MealPlan/<int:pk>/detail', views.MealPlanDetail.as_view(), name='MealPlanDetail'),
    path('accounts/', include('allauth.urls')),
    path('About', views.About, name='About'),
    path('CalcResult', views.CalcResult, name='CalcResult'),
    ]