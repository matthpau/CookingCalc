from django import forms
from .models import StoreType

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
    store_type = forms.ModelChoiceField(StoreType.objects.all(), empty_label="All stores")