#https://docs.djangoproject.com/en/2.2/ref/forms/fields/#modelchoicefield
#https://docs.djangoproject.com/en/2.2/topics/forms/

from django import forms
from .models import *

class CalcForm1(forms.Form):
    MeatType = forms.ModelChoiceField(MeatType.objects.all(), label="Meat Type ", required=True)
    CookingLevel = forms.ModelChoiceField(CookingLevel.objects.all(), label="Cooking Level ", required = True)
    EatingTime = forms.TimeField(label="When do you want to eat? (optional)", required = False)
    Weight_kg = forms.DecimalField(label="Weight of meat (kilograms) ", initial=0, required = False)
    Weight_lb = forms.DecimalField(label="or, weight of meat (pounds) ", initial=0, required = False)
    Weight_gr = forms.DecimalField(label="or, Weight of meat (grams) ", initial=0, required = False)


    # def clean(self):
    #     #Only one weight should be filled
    #     print('hitting the error checking')
    #     weights =  [
    #         self.cleaned_data.get("Weight_kg"),
    #         self.cleaned_data.get("Weight_lb"),
    #         self.cleaned_data.get("Weight_gr")
    #     ]
    #     only_pos = len([num for num in weights if int(num or 0) >0])
    #     if only_pos != 1:
    #         raise forms.ValidationError("Please put a weight in one box")

class CalcForm2(forms.Form):
    MeatType = forms.ModelChoiceField(MeatType.objects.all(), label="Meat Type ", required=True)
    CookingLevel = forms.ModelChoiceField(CookingLevel.objects.all(), label="Cooking Level ", required = True)
    EatingTime = forms.TimeField(label="When do you want to eat? (optional)", required = False)
    Count_adults = forms.IntegerField(label='Number of Adults', initial = 0, required = False)
    Count_children = forms.IntegerField(label='Number of Children', initial = 0, required = False)






