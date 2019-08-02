from django import forms
from .models import Conversion
import datetime
from django.utils.translation import gettext_lazy as _


test_text = """one partridge in a pear tree
2 turtle doves
three french hens

METHOD:
Roast the doves, french hens and partridge for seven hours then rest and serve cold, like revenge.
"""

inital_text = """Generous pinch saffron threads or powder (about 1/8 teaspoon)
1 cup warm water
8 skinless and boneless chicken  thighs, (about 21/2 pounds)
1/4 cup olive oil
Kosher salt and freshly ground black pepper
2 large onions, finely diced
4 tablespoons turmeric
4 tablespoons sumac
Cooked jasmine rice, for serving

1. In a small bowl, combine saffron and warm water. Set aside to steep until saffron dissolves and colors water. Meanwhile, pat chicken thighs dry and season all over with salt and pepper.
2. Heat olive oil in a wide, lidded pot over medium heat. Once hot, lay in chicken thighs and lightly brown both sides, about 5 minutes total. Remove chicken from pot and stir in onions. Once onions soften and turn light golden, after about 7 minutes, stir in turmeric and sauté until fragrant, about 1 minute more. Stir in sumac and saffron water to form a uniform sauce.
3. Nestle chicken thighs into pan and spoon sauce over chicken. Cover pot and lower heat to medium-low. Gently simmer until meat is tender and cooked through and sauce thickens, about 20 minutes. Check during cooking, and if sauce looks dry, add splashes of water to prevent sticking or scorching. The sauce should be wet but not soupy.
4. Serve chicken and onion sauce over rice. Bread, yogurt and/or a summer salad also make nice accompaniments.
"""



class RecipeConverter(forms.Form):

    choices = (
        (1, _("Automatic")),
        (2, _("To metric")),
        (3, _("To imperial")),
    )

    currentDT = datetime.datetime.now()
    name_initial = _('My recipe ' + currentDT.strftime("%Y-%m-%d %H:%M"))

    url_placeholder = "www.my-favourite-recipe-site.com/this-recipe.html"

    recipe_text = forms.CharField(max_length=5000, label=_('Paste or type your recipe and conversions here:'),
                                  #initial=inital_text,
                                  widget=forms.Textarea(attrs={'placeholder': test_text})
                                  )
    name = forms.CharField(max_length=200, label=_('Give your recipe a name:'), required=True,
                           initial=name_initial,
                           widget=forms.TextInput(attrs={'placeholder': _("My favourite recipe")}))
    conversion_type = forms.ChoiceField(choices=choices, initial=1)
    spoons_bool = forms.BooleanField(label=_("Don't convert spoons"), initial=True, required=False)
    cups_bool = forms.BooleanField(label=_("Don't convert cups"), initial=True, required=False)
    source_url = forms.URLField(required=False, label=_('Let us know where you got it:'),
                                widget=forms.TextInput(attrs={'placeholder': url_placeholder}))


class ConversionUpdateForm(forms.ModelForm):
    class Meta:
        model = Conversion
        fields = ['conversion_name', 'original_text', 'converted_text']


