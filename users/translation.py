from modeltranslation.translator import translator, TranslationOptions
from .models import Country

#https://django-modeltranslation.readthedocs.io/en/latest/commands.html

class CountryTranslationOptions(TranslationOptions):
    fields = ('name',) #Note final comma is necessary

translator.register(Country, CountryTranslationOptions)