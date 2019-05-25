#https://docs.djangoproject.com/en/2.2/ref/forms/fields/#modelchoicefield
#https://docs.djangoproject.com/en/2.2/topics/forms/

from django import forms
from .models import *

class CalcForm1(forms.Form):
    MeatType = forms.ModelChoiceField(MeatType.objects.all(), label="Meat Type ", required=True)
    CookingLevel = forms.ModelChoiceField(CookingLevel.objects.all(), label="Cooking Level ", required = True)
    EatingTime = forms.TimeField(label="When do you want to eat? HH:MM  (optional)", required = False, initial="00:00")
    Weight_kg = forms.DecimalField(label="Weight of meat (kilograms) ", initial=0, required = False)
    Weight_lb = forms.DecimalField(label="or, weight of meat (pounds) ", initial=0, required = False)
    Weight_g = forms.DecimalField(label="or, weight of meat (grams) ", initial=0, required = False)

    def clean(self):
        #Only one weight should be filled
        weights =  [
            self.cleaned_data.get("Weight_kg"),
            self.cleaned_data.get("Weight_lb"),
            self.cleaned_data.get("Weight_g")
            ]

        if len([num for num in weights if int(num or 0) >0]) != 1:
            print('Error')
            raise forms.ValidationError("Please put a weight in one and only one box")

class CalcForm2(forms.Form):
    MeatType = forms.ModelChoiceField(MeatType.objects.all(), label="Meat Type ", required=True)
    CookingLevel = forms.ModelChoiceField(CookingLevel.objects.all(), label="Cooking Level ", required = True)
    #EatingTime = forms.TimeField(label="When do you want to eat? HH:MM (optional)", required = False, initial="00:00")
    Count_adults = forms.IntegerField(label='Number of Adults', initial = 0, required = False, min_value=0)
    Count_children = forms.IntegerField(label='Number of Children', initial = 0, required = False, min_value=0)

    def clean(self):
        #need at least one adult or child
        weights =  [
            self.cleaned_data.get("Weight_kg"),
            self.cleaned_data.get("Weight_lb"),
            self.cleaned_data.get("Weight_gr")
        ]

        if len([num for num in weights if int(num or 0) >0]) != 1:
            raise forms.ValidationError("Please put a weight in one and only one box", code='invalid')






