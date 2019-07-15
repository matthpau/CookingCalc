#https://docs.djangoproject.com/en/2.2/ref/forms/fields/#modelchoicefield
#https://docs.djangoproject.com/en/2.2/topics/forms/
#https://github.com/monim67/django-bootstrap-datepicker-plus

from bootstrap_datepicker_plus import TimePickerInput
from django import forms
from .models import MeatType, CookingLevel, MealPlan


class CalcFormGen(forms.Form):
    MeatType = forms.ModelChoiceField(MeatType.objects.exclude(cookinginfo=None),
                                      label="What kind of meat?", required=True, empty_label='Please select')
    CookingLevel = forms.ModelChoiceField(CookingLevel.objects.none(), label="How well done?",
                                          required=True)
    EatingTime = forms.TimeField(label="When do you want to eat? HH:MM (24hr clock)",
                                 required=True, initial="14:00",
                                 widget=TimePickerInput(format='%H:%M', attrs={"class": "w-40"})
                                 )
    # w-10 needed to get the clock widget showing at 40% of width

    Weight_kg = forms.DecimalField(label="Weight of meat (kg) ", initial=0, required=False)
    Weight_lb = forms.DecimalField(label="or, weight of meat (lb) ", initial=0, required=False)
    Weight_g = forms.DecimalField(label="or, weight of meat (gr) ", initial=0, required=False)
    CountAdults = forms.IntegerField(label='Number of adults?', initial=1, required=False, min_value=0)
    CountChildren = forms.IntegerField(label='Number of children?', initial=0, required=False, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This little section is needed because we are doing dynamic ajax requests
        # It updates the allowed queryset for Cooking Levels based on the front end results of the ajax request
        # https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html

        if 'MeatType' in self.data:  # if the user has actually selected a meat type
            try:
                meat_type_id = int(self.data.get('MeatType'))

                # need to generate a proper query from CookingLevels based on Cooking Info meat_type
                html_lookup = CookingLevel.objects.filter(cookinginfo__MeatType=meat_type_id)
                self.fields['CookingLevel'].queryset = html_lookup

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

    def clean(self):
        # Only one weight should be filled
        weights = [
            self.cleaned_data.get("Weight_kg"),
            self.cleaned_data.get("Weight_lb"),
            ]

        a = len([num for num in weights if int(num or 0) > 0])
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
