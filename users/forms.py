from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from django import forms
from django.utils.translation import gettext_lazy as _

# used in the admin page
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

#https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
# general use
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'house_number',
            'street',
            'add_2',
            'add_city',
            'add_postcode',
            'add_country',
            'found_address',
            'local_offer_receive',
            'local_offer_radius']
        widgets = {
            'found_address': forms.TextInput(attrs={'readonly': True,}),
            }
        
    def clean(self):
        cleaned_data = super().clean()
        get_offers = cleaned_data.get('local_offer_receive') 
        offers_radius = cleaned_data.get('local_offer_radius')
        found_address = cleaned_data.get('found_address')

        if get_offers and offers_radius <= 0:
            raise forms.ValidationError(_("If you'd like to receive offers, please enter a valid radius"), code='invalid')

        if get_offers and not found_address:
            raise forms.ValidationError(_("Please make sure you have entered and validated your address"), code='invalid')

