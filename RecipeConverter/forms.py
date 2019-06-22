from django import forms
from .models import *
from bootstrap_datepicker_plus import TimePickerInput

test_text = """3 1/2 pounds rump roast
three cups of shit
four pounds broccoli
ddd pounds
3 1/2 pounds rump roast
1 (12 ounce) jar pickled mixed vegetables
1 (16 ounce) jar pepperoncini 
four pounds broccoli
some pounds of 4 broccoli
3.5 l of some broth
3 cups of cocaine
2 teaspoons of meth
5 tablespoons of crack
1 (.7 ounce) package dry Italian-style salad dressing mix
1 (10.5 ounce) can beef broth
5 litres of something
4.5 kg of something else

Place the roast in a 3 1/2 quart slow-cooker, and add the pickled mixed vegetables, pepperoncini, Italian dressing mix, and beef broth. Stir to blend, cover, and cook on low for 18 hours (yes, 18 hours - a light timer works well if you don't want to stay up until midnight to turn it on).
To serve, remove roast from the slow cooker. If necessary, slice it for sandwiches, but it usually just falls apart. Place the pickled vegetables and pepperoncini in a bowl to serve along with the meat.
"""


class RecipeConverter(forms.Form):

    choices = [
        (1, "Automatic"),
        (2, "To metric"),
        (3, "To imperial"),
    ]

    recipe_text = forms.CharField(max_length=5000, label='Paste your recipe here',
                                  initial=test_text, widget=forms.Textarea)
    name = forms.CharField(max_length=200, label='Give your recipe a name', required=False)
    conversion_type = forms.ChoiceField(choices=choices, initial=1)
    spoons_bool = forms.BooleanField(label="Don't convert spoons", initial=True, required=False)
    cups_bool = forms.BooleanField(label="Don't convert cups", initial=True, required=False)
    source_url = forms.URLField(required=False)


