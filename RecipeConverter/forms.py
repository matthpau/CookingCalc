from django import forms

test_text = """one partridge in a pear tree
2 turtle doves
three french hens

METHOD:
Roast the doves, french hens and partridge for seven hours then serve cold, like revenge.
"""

inital_text = """
½ cup fresh basil
2 large red kumara
2 large parsnip
1 small taro
Light olive oil or rice bran
Salt and freshly ground black pepper
Tomato sauce (makes approximately 1l)
1 cinnamon stick
2 tsp dried red chilli, chopped
2 tsp ground allspice
1.5kg ripe tomatoes
1 large onion, chopped
2 cloves garlic, chopped
1½ cups brown sugar
3/4 cup cider vinegar
1 Tbsp salt
½ cup fresh basil

1. Preheat the oven to 200C. Oil an oven tray. Peel and slice the vegetables into even sizes. Put on the tray and add more oil tossing until all are covered. Season well and toss again. Bake for 15 minutes then turn and continue cooking for approximately 15 more minutes or until all are golden and crisp.

2. To make the sauce; put all the ingredients except the basil into a saucepan and bring to a boil then reduce the heat and simmer gently for approximately 1 1/2 hours, stirring occasionally and watching to make sure the sauce doesn't become too thick.

3. Remove the cinnamon stick then process in a blender. Add the basil and pulse to combine. Taste for seasoning then pour into sterilised jars or bottles.


"""



class RecipeConverter(forms.Form):

    choices = [
        (1, "Automatic"),
        (2, "To metric"),
        (3, "To imperial"),
    ]

    url_placeholder = "www.my-favourite-recipe-site.com/this-recipe.html"

    recipe_text = forms.CharField(max_length=5000, label='Paste your recipe here:',
                                  widget=forms.Textarea(attrs={'placeholder': test_text})
                                  )
    name = forms.CharField(max_length=200, label='Give your recipe a name:', required=False,
                           widget=forms.TextInput(attrs={'placeholder': "My favourite recipe"}))
    conversion_type = forms.ChoiceField(choices=choices, initial=1)
    spoons_bool = forms.BooleanField(label="Don't convert spoons", initial=True, required=False)
    cups_bool = forms.BooleanField(label="Don't convert cups", initial=True, required=False)
    source_url = forms.URLField(required=False, label='Let us know where you got it:',
                                widget=forms.TextInput(attrs={'placeholder': url_placeholder}))

