from django.shortcuts import render
from .models import *

def Calculator(request):
    meats = MeatType.objects.all()
    cooking_info = CookingInfo.objects.all()
    context = {'meats': meats, 'cooking_info': cooking_info}
    return render(request, 'AppTimesCalc/CookingCalc.html', context)

def CalcResult(request):
    context = {'calc_inputs': request.GET}
    return render(request, 'AppTimesCalc/CookingCalcRes.html', context)

def MealPlanner(request):
    return render(request, 'AppTimesCalc/MealPlanner.html')
