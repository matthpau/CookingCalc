from django.shortcuts import render
from .models import *

def Calculator(request):
    meats = MeatType.objects.all()
    cooking_info = CookingInfo.objects.all()
    return render(request, 'AppTimesCalc/CookingCalc.html', {'meats': meats, 'cooking_info': cooking_info})

def MealPlanner(request):
    return render(request, 'AppTimesCalc/MealPlanner.html')
