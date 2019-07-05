from django import forms
#from .models import MeatType, CookingLevel, CookingInfo, MealPlan



class StoreSearch(forms.Form):
    DIST_CHOICES = [
                (1, '1km'),
                (5, '5km'),
                (20, '20km')
]

    SORT_CHOICES = [
                    ('d', 'Distance'),
                    ('v', 'Votes')
    ]

    LIMIT_CHOICES = [
        (5, '5'),
        (20, '20 '),
        (99, 'All')
    ]
    search_distance = forms.ChoiceField(choices=DIST_CHOICES, initial='5')
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, initial='d')
    results_limit = forms.ChoiceField(choices=LIMIT_CHOICES, initial='5')

