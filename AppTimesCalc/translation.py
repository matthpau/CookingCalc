from modeltranslation.translator import translator, TranslationOptions
from .models import CookingLevel, MeatType

#When you add a new field
#https://django-modeltranslation.readthedocs.io/en/latest/commands.html

class CookingLevelTranslationOptions(TranslationOptions):
    fields = ('CookingLevel',) #Note final comma is necessary

class MeatTypeTranslationOptions(TranslationOptions):
    fields = ('MeatTypeName',)

translator.register(CookingLevel, CookingLevelTranslationOptions)
translator.register(MeatType, MeatTypeTranslationOptions)
