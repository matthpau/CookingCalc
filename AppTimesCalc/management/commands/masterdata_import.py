# this is run to provide some initial values for which the database works

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('loaddata', 'dumps/MeatType.json')
        call_command('loaddata', 'dumps/CookingLevel.json')
        call_command('loaddata', 'dumps/CookingInfo.json')
        call_command('loaddata', 'dumps/Converter.json')
        call_command('loaddata', 'dumps/store_type.json')
