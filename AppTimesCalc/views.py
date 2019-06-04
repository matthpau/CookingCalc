from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import CalcForm1
from .businessLogic import CookCalc,AddMeal

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

#https://docs.djangoproject.com/en/2.2/topics/auth/default/#limiting-access-to-logged-in-users


def Home(request):
    return render(request, 'AppTimesCalc/Home.html')

def CalculatorGen(request, CalcType, ViewType):
    """
    Shows the appropriate form whether the user has selected by weight or by person
    :param request:
    :param CalcType: 'byWeight' or 'byPerson'
    :param ViewType: CookingCalc_w or CookingCalc_p
    :return:
    """

    if request.method == "POST":
        #POST, user has triggered a button

        form1 = CalcForm1(request.POST)

        if form1.is_valid():
        #this triggers the validations
            inputs = form1.cleaned_data
            inputs['CalcType'] = CalcType
            outputs = CookCalc(inputs)
            context = {'calc_inputs': inputs, 'calc_outputs': outputs}

            #Store outputs for use if the user saves later
            request.session['tempCalcOutputs'] = outputs

            if outputs['GivenWeightKg'] > 0:
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

    return render(request, 'AppTimesCalc/' + ViewType, context)

def Calculator_w(request):
    CalcType = 'byWeight'
    ViewType = "CookingCalc_w.html"
    return CalculatorGen(request, CalcType, ViewType)

def Calculator_p(request):
    CalcType = 'byPerson'
    ViewType = "CookingCalc_p.html"
    return CalculatorGen(request, CalcType, ViewType)

def MealPlannerView(request):
    return render(request, 'AppTimesCalc/MealPlanner.html')

@login_required() #this is how you decorate a function
def MealPlannerSaved(request):
    saveData = request.session['tempCalcOutputs']
    #Perform the save of the data to the MealPlans table
    AddMeal(request, saveData)

    context = {"saveData": saveData}
    return render(request, 'AppTimesCalc/MealPlannerSaved.html', context)


class MealPlanList(LoginRequiredMixin, ListView):
    #https://docs.djangoproject.com/en/2.2/topics/auth/default/#the-loginrequired-mixin
    #Context name information https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#making-friendly-template-contexts
    #template name can be used but in this case is automatically derived mealplan_list from model and view

    #context variable name is object_list OR mealplan_list, both work. Or you can set your own
    #model = MealPlan use this to show ALL meal plans

    def get_queryset(self): #this is how you return only records for the current user https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#dynamic-filtering
        return MealPlan.objects.filter(User=self.request.user).order_by('-created_at')[:5]


def About(request):
    return render(request, 'AppTimesCalc/about.html')

