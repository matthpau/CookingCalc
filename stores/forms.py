from django import forms
#from .models import MeatType, CookingLevel, CookingInfo, MealPlan



class StoreSearch(forms.Form):
    DIST_CHOICES = [
                (1, '1km'),
                (5, '5km'),
                (10, '10km'),
                (100, '100km')
                ]

    SORT_CHOICES = [
                (1,'Distance'),
                (2,'Likes')
    ]

    search_distance = forms.ChoiceField(choices=DIST_CHOICES, initial='10')
    sort_order = forms.ChoiceField(choices=SORT_CHOICES, initial='Distance')

