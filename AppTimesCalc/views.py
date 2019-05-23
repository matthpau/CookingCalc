from django.shortcuts import render
from .models import *
from .forms import CalcForm1, CalcForm2
from .businessLogic import CookCalc


def Home(request):
    return render(request, 'AppTimesCalc/Home.html')


def Calculator(request):
    if request.method == "POST":
        print('hitting post')
        my_form = CalcForm1(request.POST)
    else:
        print('hitting get')
        my_form = CalcForm1()

    meats = MeatType.objects.all()
    cooking_info = CookingInfo.objects.all()
    context = {'meats': meats, 'cooking_info': cooking_info, 'form': my_form}

    return render(request, 'AppTimesCalc/CookingCalc.html', context)


def CalcResult(request):
    inputs = request.POST
    outputs = CookCalc(inputs)
    context = {'calc_inputs': inputs, 'calc_outputs': outputs}
    return render(request, 'AppTimesCalc/CookingCalcRes.html', context)


def MealPlanner(request):
    return render(request, 'AppTimesCalc/MealPlanner.html')
