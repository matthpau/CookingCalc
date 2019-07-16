from django import forms
from .models import StoreType, AuthorisedEventEditors, Event
from users.models import CustomUser
from bootstrap_datepicker_plus import DateTimePickerInput
from django.utils.translation import gettext as _

class StoreSearch(forms.Form):
    DIST_CHOICES = [
                (1, '1km'),
                (5, '5km'),
                (10, '10km'),
                (100, '100km')
                ]

    SORT_CHOICES = [
                (1, 'Distance'),
                (2, 'Likes')
                ]

    search_distance = forms.ChoiceField(choices=DIST_CHOICES, initial='5')
    sort_order = forms.ChoiceField(choices=SORT_CHOICES, label='Sort by', initial='Distance')
    store_type = forms.ModelChoiceField(StoreType.objects.all(), empty_label="All stores")

#https://github.com/monim67/django-bootstrap-datepicker-plus/issues/15
#start = forms.DateTimeField(input_formats=["%d/%m/%Y %H:%M"], widget=DatePickerInput(format="%d/%m/%Y %H:%M").start_of('app'))

class EventAddCreate(forms.ModelForm):
    #DateTimeFormat = "%d/%m/%Y %H:%M"
    DateTimeFormat = "%d %B %Y %H:%M"

    start_date = forms.DateTimeField(
        label=_('Event start'),
        input_formats=[DateTimeFormat],
        widget=DateTimePickerInput(format=DateTimeFormat).start_of('app')
        )

    end_date = forms.DateTimeField(
        label=_('Event finish:'),
        input_formats=[DateTimeFormat],
        widget=DateTimePickerInput(format=DateTimeFormat).start_of('app'))

    class Meta:
        model = Event

        fields = ['title', 'comment', 'start_date', 'end_date', 'includes_offers']