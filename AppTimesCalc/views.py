from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import CalcForm1, CalcForm2
from .businessLogic import CookCalc

def Home(request):
    return render(request, 'AppTimesCalc/Home.html')

def Calculator(request):
    meats = MeatType.objects.all()
    cooking_info = CookingInfo.objects.all()

    if request.method == "POST":
        #POST, user has triggered a button

        form1 = CalcForm1(request.POST)
        form2 = CalcForm2(request.POST)

        if 'Calculator1' in request.POST:
        #user triggered the first form

            if form1.is_valid():
                inputs = form1.cleaned_data
                outputs = CookCalc(inputs)
                context = {'calc_inputs': inputs, 'calc_outputs': outputs}
                return render(request, 'AppTimesCalc/CookingCalcRes.html', context)

        elif 'Calculator2' in request.POST:
            return HttpResponse('You hit the second button')

    else:
        form1 = CalcForm1()
        form2 = CalcForm2()

    context = {'meats': meats,
               'cooking_info': cooking_info,
               'form1': form1,
               'form2': form2
               }

    return render(request, 'AppTimesCalc/CookingCalc.html', context)


def CalcResult(request):
    print(request.GET)
    #outputs = CookCalc(inputs)
    #context = {'calc_inputs': inputs, 'calc_outputs': outputs}
    #return render(request, 'AppTimesCalc/CookingCalcRes.html', context)
    #return HttpResponse("You made it to the CalcResult")


def MealPlanner(request):
    return render(request, 'AppTimesCalc/MealPlanner.html')
