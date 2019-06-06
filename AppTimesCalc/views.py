from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import *
from .forms import CalcFormPerson, CalcFormWeight, mealPlanComment
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

def CalculatorGen(request, CalcType):
    """
    Shows the appropriate form whether the user has selected by weight or by person
    :param request:
    :param CalcType: 'byWeight' or 'byPerson'
    :param ViewType: CookingCalc_w or CookingCalc_p
    :return:
    """

    if CalcType == 'byWeight':
        MyForm = CalcFormWeight
    elif CalcType == 'byPerson':
        MyForm = CalcFormPerson
    else:
        pass

    if request.method == "POST":
        # POST, user has triggered a button

        form1 = MyForm(request.POST)

        if form1.is_valid():
        # this triggers the validations
            inputs = form1.cleaned_data
            inputs['CalcType'] = CalcType

            outputs = CookCalc(inputs)

            context = {'calc_inputs': inputs,
                       'calc_outputs': outputs,
                       'form': mealPlanComment()}

            if outputs['GivenWeightKg'] > 0:
                request.session['tempCalcOutputs'] = outputs # Store outputs for use if the user saves later
                return render(request, 'AppTimesCalc/CookingCalcRes.html', context)
            else:
                return render(request, 'AppTimesCalc/CookingCalcResError.html')

    else:
        form1 = MyForm()
        #this is the GET for initial display

    meats = MeatType.objects.all()
    cooking_info = CookingInfo.objects.all()
    context = {'meats': meats,
               'cooking_info': cooking_info,
               'form1': form1,
               }

    return render(request, 'AppTimesCalc/CookingCalc.html', context)

def Calculator_w(request):
    CalcType = 'byWeight'
    return CalculatorGen(request, CalcType)

def Calculator_p(request):
    CalcType = 'byPerson'
    return CalculatorGen(request, CalcType)

def CalcResult(request, context):
    return render(request, 'AppTimesCalc/CookingCalcRes.html', context)

@login_required() #this is how you decorate a function
def MealPlannerSaved(request):


    saveData = request.session['tempCalcOutputs'] # Get the save data from the session
    saveData['planName'] = request.POST['MealComment'] # Get the (optional) plan name given
    print(saveData)

    #Perform the save of the data to the MealPlans table
    x = AddMeal(request, saveData) # returns PK of the newly saved record

    context = {"saveData": saveData, "savePK": x}
    return render(request, 'AppTimesCalc/MealPlannerSaved.html', context)


class MealPlanList(LoginRequiredMixin, ListView):
    #requires login, use LoginRequiredMixin to do this
    #https://docs.djangoproject.com/en/2.2/topics/auth/default/#the-loginrequired-mixin
    #Context name information https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#making-friendly-template-contexts
    #template name can be used but in this case is automatically derived mealplan_list from model and view

    #context variable name is object_list OR mealplan_list, both work. Or you can set your own
    #model = MealPlan use this to show ALL meal plans

    def get_queryset(self): #this is how you return only records for the current user https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#dynamic-filtering
        return MealPlan.objects.filter(User=self.request.user).order_by('-created_at')[:5]


def About(request):
    return render(request, 'AppTimesCalc/about.html')

