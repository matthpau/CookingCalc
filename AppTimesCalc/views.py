from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import CalcFormPerson, CalcFormWeight, mealPlanComment, MealPlanForm
from .businessLogic import CookCalc, AddMeal

from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from users.models import CustomUser


# https://docs.djangoproject.com/en/2.2/topics/auth/default/#limiting-access-to-logged-in-users


def Home(request):
    return render(request, 'AppTimesCalc/Home.html')


def About(request):
    return render(request, 'AppTimesCalc/about.html')


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
                request.session['tempCalcOutputs'] = outputs  # Store outputs for use if the user saves later
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


#@login_required()
# this is how you decorate a function. Would have used this but then the request.POST['MealComment'] disappears
def MealPlannerSaved(request):

    # Grab the comment

    if not request.user.is_authenticated:
        request.session['planName'] = request.POST['MealComment']
        request.session['redirected'] = True
        # print('Need to login')
        return redirect('accounts/login' '/?next=/MealPlannerSaved')

    else:
        # User was already authenticated
        saveData = request.session['tempCalcOutputs']  # Get the save data from the session
        saveData['User'] = request.user

        if request.session.get('redirected', False): # the comment was already captured before redirecting to the login
            saveData['planName'] = request.session['planName']  # get it from the session
        else:
            saveData['planName'] = request.POST['MealComment']  # get it from the form

        request.session['redirected'] = False  # reset the redirect flag

        # Perform the save of the data to the MealPlans table
        x = AddMeal(saveData)  # returns PK of the newly saved record

        context = {"saveData": saveData}
        return render(request, 'AppTimesCalc/MealPlannerSaved.html', context)


class MealPlanList(LoginRequiredMixin, ListView):
    """
    requires login, use LoginRequiredMixin to do this
    https://docs.djangoproject.com/en/2.2/topics/auth/default/#the-loginrequired-mixin
    Context name information https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#making-friendly-template-contexts
    template name can be used but in this case is automatically derived mealplan_list from model and view

    context variable name is object_list OR mealplan_list, both work. Or you can set your own
     model = MealPlan use this to show ALL meal plans
    """
    def get_queryset(self):
        #  this is how you return only records for the current user
        #  https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#dynamic-filtering
        return MealPlan.objects.filter(User=self.request.user).order_by('-created_at')  # [:5]

#TODO can delete?
class MealPlanDetail(DetailView):
    queryset = MealPlan.objects.all()
    # Automatically looks for mealplan_detail.html


class MealPlanUpdate(UpdateView):
    form_class = MealPlanForm
    template_name = 'AppTimesCalc/mealplan_update.html'
    success_url = '/MealPlanList'

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(MealPlan, id=id_)


    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


def MealPlanDelete(request, pk):

    if request.method == 'POST':

        CurrentRecord = MealPlan.objects.get(id=pk)

        #  Check we are the logged in user for security
        if request.user == CurrentRecord.User:

            # needs to be filter rather than get so that .exists() works
            a = CustomUser.objects.filter(username=settings.ARCHIVE_USERNAME)
            if not a.exists():
                b = CustomUser(username=settings.ARCHIVE_USERNAME, email=settings.ARCHIVE_USER_EMAIL)
                b.save()

            #Change the record in Meal PLan to the archive user
            CurrentRecord.User = CustomUser.objects.get(username=settings.ARCHIVE_USERNAME)
            # Could also clear out comments e.g. CurrentRecord.PlanName= '' etc
            CurrentRecord.save()

        return HttpResponseRedirect('/MealPlanList')

    else:
        PlanName = MealPlan.objects.get(id=pk).friendlyname()
        context = {"MealPlanName": PlanName}
        return render(request, 'AppTimesCalc/mealplan_confirm_delete.html', context)


def load_cooking_levels(request):
    meat_type = request.GET.get('MeatTypeID')
    cooking_levels = CookingLevel.objects.filter(cookinginfo__MeatType=meat_type)
    # WRONG
    # cooking_levels = CookingInfo.objects.filter(MeatType=meat_type)
    return render(request, 'AppTimesCalc/cooking_level_list_options.html', {'CookingLevels': cooking_levels})