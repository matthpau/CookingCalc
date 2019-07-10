# this is run to provide some initial values for which the database works

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('dumpdata', 'AppTimesCalc.MeatType', '--output=dumps/MeatType.json')
        call_command('dumpdata', 'AppTimesCalc.CookingLevel', '--output=dumps/CookingLevel.json')
        call_command('dumpdata', 'AppTimesCalc.CookingInfo', '--output=dumps/CookingInfo.json')
        call_command('dumpdata', 'RecipeConverter.Converter', '--output=dumps/Converter.json')
        call_command('dumpdata', 'stores.StoreType', '--output=dumps/store_type.json')