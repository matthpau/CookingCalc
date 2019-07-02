# this is run to provide some initial values for which the database works

from django.core.management.base import BaseCommand

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/


class Command(BaseCommand):

    def handle(self, *args, **options):
        import django
        import json
        from os.path import expanduser, isfile
        from django.contrib.gis.geos import fromstr
        from django.apps import apps
        from django.db.utils import IntegrityError

        #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CookingBase.settings")
        #django.setup()

        from stores.models import Store


        def delete_data():
            Store.objects.all().delete()

        def load_data(filename):

            DATA_PATH = expanduser('~/matthpau.pythonanywhere.com/CookingCalc/dumps/store_import/')
            if isfile(DATA_PATH + filename):   # this is valid for linux
                jsonfile = DATA_PATH + filename
            else:
                DATA_PATH = '../CookingBase/dumps/store_import/'
                if isfile(DATA_PATH + filename):  # this is valid for local mac
                    print('found data file for mac')
                    jsonfile = DATA_PATH + filename

            i = 0
            Shop = apps.get_model('stores', 'Store')
            with open(str(jsonfile)) as datafile:
                objects = json.load(datafile)
                for obj in objects['elements']:
                    try:
                        objType = obj['type']
                        if objType == 'node':
                            tags = obj['tags']
                            store_name = tags.get('name', 'no-name')
                            longitude = obj.get('lon', 0)
                            latitude = obj.get('lat', 0)
                            location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                            osmid = obj.get('id', 0)

                            try:
                                s = Shop(name=store_name,
                                         location=location,
                                         add_house_number=tags.get('addr:housenumber', ''),
                                         add_street=tags.get('addr:street', ''),
                                         add_postcode=tags.get('addr:postcode', 'unknown'),
                                         add_city=tags.get('addr:city', 'unknown'),
                                         add_country=tags.get('addr:country', 'unknown'),
                                         OSM_ID=osmid,
                                         lat=latitude,
                                         long=longitude,
                                         )
                                s.save()
                                i += 1

                            except IntegrityError:
                                print(osmid, 'already exists, skipping')
                                # store already exists, has OSM_ID in database
                                pass
                    except KeyError:
                        pass
            print(i, 'stores loaded')

        print('clearing table')
        delete_data()
        print('loading table')
        load_data('germany.json')