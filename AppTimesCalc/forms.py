#https://docs.djangoproject.com/en/2.2/ref/forms/fields/#modelchoicefield
#https://docs.djangoproject.com/en/2.2/topics/forms/
#https://github.com/monim67/django-bootstrap-datepicker-plus

from django import forms
from .models import *
from bootstrap_datepicker_plus import TimePickerInput

from allauth.account.forms import SignupForm, LoginForm


class CalcFormGen(forms.Form):
    MeatType = forms.ModelChoiceField(MeatType.objects.all(), label="Meat Type ", required=True, initial="Beef")
    CookingLevel = forms.ModelChoiceField(CookingLevel.objects.all(), label="Cooking Level ", required=True, initial = "Rare")
    EatingTime = forms.TimeField(label="When do you want to eat? HH:MM (24hr clock)",
                                 required=True, initial="14:00",
                                 widget=TimePickerInput(format='%H:%M',attrs={"class": "w-40"})
                                 )
                                #w-10 needed to get the clock widget showing at 40% of width
    Weight_kg = forms.DecimalField(label="Weight of meat (kilograms) ", initial=3.14, required=False)
    Weight_lb = forms.DecimalField(label="or, weight of meat (pounds) ", initial=0, required=False)
    Weight_g = forms.DecimalField(label="or, weight of meat (grams) ", initial=0, required=False)
    CountAdults = forms.IntegerField(label='Number of adults', initial=1, required=False, min_value=0)
    CountChildren = forms.IntegerField(label='Number of children', initial=0, required=False, min_value=0)


    def clean(self):
        #Only one weight should be filled
        weights =  [
            self.cleaned_data.get("Weight_kg"),
            self.cleaned_data.get("Weight_lb"),
            self.cleaned_data.get("Weight_g")
            ]

        a = len([num for num in weights if int(num or 0) >0])
        if a > 1:
            raise forms.ValidationError("Please put a weight in one and only one box")


class CalcFormPerson(CalcFormGen):
    # this is used when calculating by person, we therefore don't need the weights
    # https://docs.djangoproject.com/en/2.2/ref/forms/api/#subclassing-forms
    Weight_kg = None
    Weight_lb = None
    Weight_g = None


class CalcFormWeight(CalcFormGen):
    # this is used when calculating by weight, we therefore don't need the people
    CountAdults = None
    CountChildren = None

# https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/


class mealPlanComment(forms.Form):
    MealComment = forms.CharField(max_length=200, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'My plan name (optional)',
                                                                "class": "w-100", }))


class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ['PlanName', 'RatingStars', 'RatingComment', 'RatingResult']
        widgets = {'RatingComment': forms.Textarea(attrs={'rows': 3})}
