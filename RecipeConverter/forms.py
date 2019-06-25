from django import forms

test_text = """one partridge in a pear tree
2 turtle doves
three french hens

METHOD:
Roast the doves, french hens and partridge for seven hours then serve cold, like revenge.
"""

inital_text = """1/2 cup flour
10 l coke
15 kg chicken
2.5 kg chicken

Turn the oven on to 200degC
"""



class RecipeConverter(forms.Form):

    choices = [
        (1, "Automatic"),
        (2, "To metric"),
        (3, "To imperial"),
    ]

    url_placeholder = "www.my-favourite-recipe-site.com/this-recipe.html"

    recipe_text = forms.CharField(max_length=5000, label='Paste your recipe here:', initial=inital_text,
                                  widget=forms.Textarea(attrs={'placeholder': test_text})
                                  )
    name = forms.CharField(max_length=200, label='Give your recipe a name:', required=False,
                           widget=forms.TextInput(attrs={'placeholder': "My favourite recipe"}))
    conversion_type = forms.ChoiceField(choices=choices, initial=1)
    spoons_bool = forms.BooleanField(label="Don't convert spoons", initial=True, required=False)
    cups_bool = forms.BooleanField(label="Don't convert cups", initial=True, required=False)
    source_url = forms.URLField(required=False, label='Let us know where you got it:',
                                widget=forms.TextInput(attrs={'placeholder': url_placeholder}))

