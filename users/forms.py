from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from django import forms

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
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['add_1', 'add_2', 'add_city', 'add_postcode', 'add_country', 'found_address',
        'local_offer_receive', 'local_offer_radius', 'temp_address']
        #widgets = {'found_address': forms.TextInput(attrs={'disabled': True})}
        
    def clean(self):
        cleaned_data = super().clean()
        get_offers = cleaned_data.get('local_offer_receive') 
        offers_radius = cleaned_data.get('local_offer_radius')

        if get_offers and offers_radius <= 0:
            raise forms.ValidationError("If you'd like to receive offers, please enter a valid radius")

