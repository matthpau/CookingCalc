# this is run to provide some initial values for which the database works

from django.core.management.base import BaseCommand

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/


class Command(BaseCommand):

    def handle(self, *args, **options):
        import django
        import json
        from os.path import expanduser, isfile
        from os import listdir
        from django.contrib.gis.geos import fromstr
        from django.apps import apps
        from django.db.utils import IntegrityError, DataError

        #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CookingBase.settings")
        #django.setup()

        from stores.models import Store


        def delete_data():
            Store.objects.all().delete()

        def load_data(filename):

            DATA_PATH = expanduser('~/matthpau.pythonanywhere.com/CookingCalc/dumps/store_import/')
            if isfile(DATA_PATH + filename):   # this is valid for linux
                print('found data file for linux/python anywhere, loading')
                jsonfile = DATA_PATH + filename
            else:
                DATA_PATH = '../CookingBase/dumps/store_import/'
                if isfile(DATA_PATH + filename):  # this is valid for local mac
                    print('found data file for mac, loading')
                    jsonfile = DATA_PATH + filename

            i = 0
            skipped = 0
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
                                         lon=longitude,
                                         )
                                s.save()
                                i += 1

                            except IntegrityError:
                                #print(osmid, 'already exists, skipping')
                                skipped += 1
                                # store already exists, has OSM_ID in database
                                pass
                            except DataError:
                                print('Problem with', obj)
                                print()
                                pass

                    except KeyError:
                        pass
            print(i, 'stores loaded, ', skipped, 'stores skipped')

        #print('clearing table')
        #delete_data()

        print('loading table')
        print('Loading Germany')
        load_data('germany.json')
        print('Loading England')
        load_data('england.json')
        print('Loading Croatia')
        load_data('croatia.json')
        print('Loading France')
        load_data('france.json')
        print('Loading Australia')
        load_data('australia.json')
        print('Loading NZ')
        load_data('nz.json')
        print('Loading Ireland')
        load_data('ireland.json')
        print('Loading USA')
        load_data('usa.json')
        print('Loading Spain')
        load_data('spain.json')
        print('Loading South Africa')
        load_data('za.json')
        print('Loading Brazil')
        load_data('brazil.json')
        print('Loading UK')
        load_data('uk.json')
        print('Loading Canada')
        load_data('canada.json')




