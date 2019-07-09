# this is run to provide some initial values for which the database works

import time
from django.core.management.base import BaseCommand
from django.conf import settings
import requests

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):
        import json
        from os.path import expanduser, isfile
        import os
        from django.contrib.gis.geos import fromstr
        from django.apps import apps
        from django.db.utils import IntegrityError, DataError


        from stores.models import Store
        import_folder = 'dumps/store_import'

        def delete_data():
            Store.objects.all().delete()
            print('All records have been deleted')
            print()

        def get_data_from_OSM(country_name, country_code):
            was_replaced = False
            max_file_age = 7 * 24 * 60 * 60  #how old a file needs to be before it is replace, secs
            country_name = country_name.replace(' ', '_').lower()
            save_file = os.path.join(settings.BASE_DIR, import_folder, country_name + '.json')
            print('downloading', country_name, 'to', save_file)

            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
[out:json][timeout:1000];
area["ISO3166-1"="{country_code}"][admin_level=2];
nwr(area)["shop"="butcher"];
out center;
"""
            replace_flag = False

            if isfile(save_file):
                file_age = time.time() - os.path.getmtime(save_file)
                if file_age > max_file_age:
                    replace_flag = True
                    os.remove(save_file)
                    print('Old file expired, has been removed')
                else:
                    print('File still up to date, keeping existing')
            else:
                replace_flag = True

            if replace_flag:
                print('getting update')
                r = requests.get(overpass_url, params={'data': overpass_query})
                if r.status_code == 200:
                    with open(save_file, 'w') as f:
                        json.dump(r.json(), f)
                        print('File write complete')
                        was_replaced = True
                else:
                    print('failed', r.status_code)
                    print('url', r.url)
                    print('query', overpass_query)

            print()
            return was_replaced

        def load_data(country_name, country_code):
            from stores.models import Country
            nice_name = country_name
            country_name = country_name.replace(' ', '_').lower()

            #Add country to list of countries if not there
            c, created = Country.objects.get_or_create(
                pk=country_code,
                defaults={'name':nice_name}
                )

            import_file_prod = expanduser(os.path.join('~/matthpau.pythonanywhere.com/CookingCalc/', import_folder, country_name + '.json'))
            import_file_dev = os.path.join(settings.BASE_DIR, import_folder, country_name + '.json')

            if isfile(import_file_prod):   # this is valid for prod linux
                import_file = import_file_prod
                print('found data file for linux/python anywhere, loading')
            elif isfile(import_file_dev):   # valid for local mac
                import_file = import_file_dev
                print('found data file for mac, loading', country_name)
            else:
                print('no file found, skipping')
                import_file = None

            if import_file:
                i = 0
                skipped = 0

                shop = apps.get_model('stores', 'Store')

                #Import file
                with open(str(import_file)) as datafile:
                    objects = json.load(datafile)
                    for obj in objects['elements']:
                        try:
                            obj_type = obj['type']
                            if obj_type == 'node':
                                tags = obj['tags']
                                store_name = tags.get('name', 'no-name')
                                longitude = obj.get('lon', 0)
                                latitude = obj.get('lat', 0)
                                location = fromstr(f'POINT({longitude} {latitude})', srid=4326)
                                osmid = obj.get('id', 0)

                                #Put together a street address
                                address = tags.get('addr:housenumber', '') + ' ' + \
                                    tags.get('addr:street', '') +', ' + \
                                    tags.get('addr:city', '') + ', ' + \
                                    tags.get('addr:country', '') + ' ' + \
                                    tags.get('addr:postcode', '')

                                address = address.lstrip().rstrip()

                                if address == ' , ,  ': # nothing was there
                                    address = None

                                while address and address[-1] in (' ', ','):
                                    address = address[:-1]

                                address = address.replace(', , ', ', ')

                                if not address:
                                    address = ''

                                try:
                                    s = shop(name=store_name,
                                             my_name=store_name,
                                             my_address=address,
                                             my_country=c,
                                             location=location,
                                             add_house_number=tags.get('addr:housenumber', ''),
                                             add_street=tags.get('addr:street', ''),
                                             add_postcode=tags.get('addr:postcode', ''),
                                             add_city=tags.get('addr:city', ''),
                                             add_country=tags.get('addr:country', ''),
                                             OSM_ID=osmid,
                                             lat=latitude,
                                             lon=longitude,
                                             )
                                    s.save()
                                    i += 1

                                except IntegrityError:
                                    skipped += 1
                                except DataError:
                                    print('Problem with', obj)
                                    print()

                        except KeyError:
                            pass
                print(i, 'stores loaded, ', skipped, 'stores skipped')
                print()

        # https://www.nationsonline.org/oneworld/country_code_list.htm
        country_list = {
            'Croatia': 'HR',
            'Great Britain': 'GB',
            'New zealand': 'NZ',
            'Ireland': 'IE',
            'South Africa': 'ZA',
            'Canada': 'CA',
            'Jamaica': 'JM',
            'Germany': 'DE',
            'United States': 'US'
        }

        #get latest from OSM

        delete_data()

        country_count = len(country_list)
        i = 0
        for k, v in country_list.items():
            i += 1
            x = get_data_from_OSM(k, v)
            if x and i != country_count:
                print('Waiting a bit before I do the next one...')
                time.sleep(20)

        for k, v in country_list.items():
            load_data(k, v)
