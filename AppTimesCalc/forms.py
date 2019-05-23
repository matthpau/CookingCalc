#https://docs.djangoproject.com/en/2.2/ref/forms/fields/#modelchoicefield
#https://docs.djangoproject.com/en/2.2/topics/forms/

from django import forms
from .models import *

class CalcForm(forms.Form):
    Weight = forms.FloatField(label="Weight of meat (kg) ", required=True)
    CookingLevel = forms.ModelChoiceField(CookingLevel.objects.all(), label="Cooking Level ", required = True)
    MeatType = forms.ModelChoiceField(MeatType.objects.all(), label = "Meat Type ", required = True)


