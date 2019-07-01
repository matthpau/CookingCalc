from django.core.management import call_command
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CookingBase.settings")
django.setup()

# call_command('dumpdata', '--output=dumps/datadump.json')
call_command('dumpdata', 'AppTimesCalc.MeatType', '--output=dumps/MeatType.json')
call_command('dumpdata', 'AppTimesCalc.CookingLevel', '--output=dumps/CookingLevel.json')
call_command('dumpdata', 'AppTimesCalc.CookingInfo', '--output=dumps/CookingInfo.json')
call_command('dumpdata', 'RecipeConverter.Converter', '--output=dumps/Converter.json')





