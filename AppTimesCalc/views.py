from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import CalcForm1
from .businessLogic import CookCalc

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


def Home(request):
    return render(request, 'AppTimesCalc/Home.html')

def Calculator_w(request):

    if request.method == "POST":
        #POST, user has triggered a button

        form1 = CalcForm1(request.POST)

        #What kind of calculation type? By weight or by person?

        if form1.is_valid():
        #this triggers the validations
            inputs = form1.cleaned_data
            inputs['CalcType'] = 'byWeight'
            outputs = CookCalc(inputs)
            context = {'calc_inputs': inputs, 'calc_outputs': outputs}

            if outputs['givenWeightKg'] > 0:
                return render(request, 'AppTimesCalc/CookingCalcRes1.html', context)
            else:
                return render(request, 'AppTimesCalc/CookingCalcRes1Error.html')

    else:
        form1 = CalcForm1()
        #this is the GET for initial display

    meats = MeatType.objects.all()
    cooking_info = CookingInfo.objects.all()
    context = {'meats': meats,
               'cooking_info': cooking_info,
               'form1': form1,
               }

    return render(request, 'AppTimesCalc/CookingCalc_w.html', context)

def Calculator_p(request):

    if request.method == "POST":
        #POST, user has triggered a button

        form1 = CalcForm1(request.POST)

        #What kind of calculation type? By weight or by person?

        if form1.is_valid():
        #this triggers the validations
            inputs = form1.cleaned_data
            inputs['CalcType'] = 'byPerson'
            outputs = CookCalc(inputs)
            context = {'calc_inputs': inputs, 'calc_outputs': outputs}

            if outputs['givenWeightKg'] > 0:
                return render(request, 'AppTimesCalc/CookingCalcRes1.html', context)
            else:
                return render(request, 'AppTimesCalc/CookingCalcRes1Error.html')

    else:
        form1 = CalcForm1()
        #this is the GET for initial display

    meats = MeatType.objects.all()
    cooking_info = CookingInfo.objects.all()
    context = {'meats': meats,
               'cooking_info': cooking_info,
               'form1': form1,
               }

    return render(request, 'AppTimesCalc/CookingCalc_p.html', context)


def CalcResult(request):
    print(request.GET)
    #outputs = CookCalc(inputs)
    #context = {'calc_inputs': inputs, 'calc_outputs': outputs}
    #return render(request, 'AppTimesCalc/CookingCalcRes.html', context)
    #return HttpResponse("You made it to the CalcResult")


def MealPlannerView(request):
    return render(request, 'AppTimesCalc/MealPlanner.html')


def MealPlannerSaved(request):
    return render(request, 'AppTimesCalc/MealPlannerSaved.html')

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def About(request):
    return render(request, 'AppTimesCalc/about.html')

class MealPlanDetail(generic.ListView):
    model = MealPlan
    #https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/
    #Template name is inferred from generic view: AppTimesCalc/mealplan_list.html
