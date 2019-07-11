# this is run to provide some initial values for which the database works

from datetime import datetime as dt
import os, shutil
from django.core.management.base import BaseCommand
from django.core.management import call_command

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        # Copy existing files to a named backup folder
        dumps_folder = 'dumps/'
        ct = dt.now()
        save_folder = '_'.join([
            str(ct.year),
            str(ct.month),
            str(ct.day),
            str(ct.hour),
            str(ct.minute),
            str(ct.second)
            ])
        new_folder_path = os.path.join(dumps_folder, save_folder)
        
        os.mkdir(new_folder_path)
        files = os.listdir(dumps_folder)
        for file in files:
            if file.endswith('.json'):
                source = os.path.join(dumps_folder, file)
                dest = os.path.join(new_folder_path, file)

                shutil.copy(source, dest)


        call_command('dumpdata', 'AppTimesCalc.MeatType', f'--output={dumps_folder}/MeatType.json')
        call_command('dumpdata', 'AppTimesCalc.CookingLevel', f'--output={dumps_folder}/CookingLevel.json')
        call_command('dumpdata', 'AppTimesCalc.CookingInfo', f'--output={dumps_folder}/CookingInfo.json')
        call_command('dumpdata', 'RecipeConverter.Converter', f'--output={dumps_folder}/Converter.json')
        call_command('dumpdata', 'stores.StoreType', f'--output={dumps_folder}/store_type.json')