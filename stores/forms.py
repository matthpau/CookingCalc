from django import forms
from .models import StoreType, AuthorisedEventEditors, Event
from users.models import CustomUser
from bootstrap_datepicker_plus import DatePickerInput
from django.utils.translation import gettext_lazy as _


class StoreSearch(forms.Form):
    DIST_CHOICES = (
        (2, '2km'),
        (5, '5km'),
        (10, '10km'),
        (50, '50km')
    )

    SORT_CHOICES = (
        (1, _('Distance')),
        (2, _('Likes'))
    )

    FROM_CHOICES = (
        (1, "Current Location"),
        (2, "Profile Address")
    )

    search_from = forms.ChoiceField(
        choices=FROM_CHOICES, label=_('Search From'), initial='1')
    search_distance = forms.ChoiceField(
        choices=DIST_CHOICES, label=_('Search Distance'), initial='5')
    sort_order = forms.ChoiceField(
        choices=SORT_CHOICES, label=_('Sort by'), initial=_('Distance'))
    store_type = forms.ModelChoiceField(StoreType.objects.all(), label=_(
        'Store Type'), empty_label=_("All stores"))


# https://github.com/monim67/django-bootstrap-datepicker-plus/issues/15
#start = forms.DateTimeField(input_formats=["%d/%m/%Y %H:%M"], widget=DatePickerInput(format="%d/%m/%Y %H:%M").start_of('app'))

class EventAddCreate(forms.ModelForm):
    #DateTimeFormat = "%d/%m/%Y %H:%M"
    DateTimeFormat = "%d %B %Y"

    start_date = forms.DateTimeField(
        label=_('Event start'),
        input_formats=[DateTimeFormat],
        widget=DatePickerInput(format=DateTimeFormat).start_of('app')
    )

    end_date = forms.DateTimeField(
        label=_('Event finish:'),
        input_formats=[DateTimeFormat],
        widget=DatePickerInput(format=DateTimeFormat).start_of('app'))

    class Meta:
        model = Event

        fields = ['title', 'comment', 'start_date',
                  'end_date', 'includes_offers']
