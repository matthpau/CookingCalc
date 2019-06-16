from django.urls import include, path
from . import views

from django.conf import settings
from django.conf.urls.static import static

#https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/

urlpatterns = [
    path('', views.Home, name='Home'),
    path('Calculator_w', views.Calculator_w, name='Calculator_w'),
    path('Calculator_p', views.Calculator_p, name='Calculator_p'),
    path('MealPlannerSaved', views.MealPlannerSaved, name='MealPlannerSaved'),
    path('MealPlanList', views.MealPlanList.as_view(), name='MealPlanList'),
    path('MealPlan/<int:pk>/update', views.MealPlanUpdate.as_view(), name='MealPlanUpdate'),
    path('MealPlan/<int:pk>/detail', views.MealPlanDetail.as_view(), name='MealPlanDetail'),
    path('MealPlan/<int:pk>/delete', views.MealPlanDelete, name='MealPlanDelete'),
    path('accounts/', include('allauth.urls')),
    path('About', views.About, name='About'),
    path('CalcResult', views.CalcResult, name='CalcResult'),
    path('ajax/load_cooking_levels/', views.load_cooking_levels, name='ajax_load_cooking_levels'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# https://docs.djangoproject.com/en/2.2/howto/static-files/
