from django.shortcuts import render
from .models import *
from .forms import CalcForm
from .businessLogic import CookCalc



def Home(request):
    return render(request, 'AppTimesCalc/Home.html')

def Calculator(request):
    meats = MeatType.objects.all()
    cooking_info = CookingInfo.objects.all()
    context = {'meats': meats, 'cooking_info': cooking_info, 'form': CalcForm()}
    return render(request, 'AppTimesCalc/CookingCalc.html', context)

def CalcResult(request):
    inputs = request.GET
    outputs = CookCalc(inputs)
    context = {'calc_inputs': inputs, 'calc_outputs': outputs}
    return render(request, 'AppTimesCalc/CookingCalcRes.html', context)

def MealPlanner(request):
    return render(request, 'AppTimesCalc/MealPlanner.html')
