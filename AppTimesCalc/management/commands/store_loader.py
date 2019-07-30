# this is run to provide some initial values for which the database works


from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from stores.models import Store

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):
        import json
        from os.path import expanduser, isfile, join
        import os
        import datetime as dt
        import time
        from django.contrib.gis.geos import fromstr
        from django.apps import apps
        from django.db.utils import IntegrityError, DataError
        from stores.models import Store, StoreType, Country
        IMPORT_FOLDER = 'dumps/store_import'
        LOGS_FOLDER = 'logs/store_load'


        def delete_data():
            print('clearing all records')
            Store.objects.all().delete()
            print('all records have been deleted')
            print()

        #https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
        def get_data_from_OSM(country_name, country_code, osm_shops, fresh=False, max_days=2):
            """
            fresh True forces a download regardless of file age
            maxAge in days how old a file should be before being replaced
            """
            was_replaced = False
            
            if fresh:
                max_file_age = 0
            else:   
                max_file_age = max_days * 24 * 60 * 60  #how old a file needs to be before it is replace, secs
            country_name = country_name.replace(' ', '_').lower()
            save_file = join(settings.BASE_DIR, IMPORT_FOLDER, country_name + '.json')
            logfile.write('getting data for ' + country_name + ' using savefile: ' + save_file + '\n')

            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
            [out:json][timeout:1000];
            area["ISO3166-1"="{country_code}"][admin_level=2]->.searchArea;
            """
            from stores.models import StoreType

            for elt in osm_shops:
                shop_text = f"""
                node(area.searchArea)["shop"="{elt}"];
                out center;
                """
                overpass_query += shop_text

                #Add storetype to list of storetypes if not there
                c, created = StoreType.objects.get_or_create(
                    pk=elt,
                    defaults={'icon_text': 'Font awesome icon here please'}
                    )  

            replace_flag = False

            if isfile(save_file):
                file_age = time.time() - os.path.getmtime(save_file)
                if file_age > max_file_age:
                    replace_flag = True
                    os.remove(save_file)
                    logfile.write('Old file expired, has been removed\n')
                else:
                    logfile.write('File still up to date, keeping existing\n')
            else:
                replace_flag = True

            if replace_flag:
                logfile.write('File out of date, getting update from OSM\n')
                r = requests.get(overpass_url, params={'data': overpass_query})
                if r.status_code == 200:
                    with open(save_file, 'w') as f:
                        json.dump(r.json(), f)
                        logfile.write('Local save complete\n')
                        was_replaced = True
                else:
                    logfile.write('failed, code: ' + str(r.status_code) + '\n')
                    if r.status_code == 429:
                        logfile.write('Code 429 means: too much work for OpenStreetMap\n')
                    else:
                        logfile.write('Some other streetmap error. Details:\n')
                        logfile.write('url:' + r.url+ '\n')
                        logfile.write('query:' + overpass_query+ '\n')

            logfile.write('\n')
            return was_replaced

        def make_website(url_text):
            result = ''
            if url_text:
                if url_text[:4] != 'http':
                    result = 'http://' + url_text
                else:
                    result = url_text
            else:
                result = ''

            return result

        def load_data(country_name, country_code, logfile):
            """
            logfile is unique per overall run
            """

            nice_name = country_name
            country_name = country_name.replace(' ', '_').lower()

            #Add country to list of countries if not there
            country, created = Country.objects.get_or_create(
                pk=country_code,
                defaults={'name':nice_name}
                )

            import_file_prod = expanduser(join('~/matthpau.pythonanywhere.com/CookingCalc/', IMPORT_FOLDER, country_name + '.json'))
            import_file_dev = join(settings.BASE_DIR, IMPORT_FOLDER, country_name + '.json')

            if isfile(import_file_prod):   # this is valid for prod linux
                import_file = import_file_prod
                logfile.write('    found data file for linux/python anywhere, loading\n')
            elif isfile(import_file_dev):   # valid for local mac
                import_file = import_file_dev
                logfile.write('    found data file for mac, loading ' + country_name + '\n')
            else:
                logfile.write('    no file found, skipping\n')
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
                                store_name = tags.get('name', tags.get('shop') + ', name unknown')
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

                                o = StoreType.objects.get(pk=tags.get('shop', ''))

                                try:
                                    s = shop(name=store_name,
                                             my_name=store_name,
                                             my_address=address,
                                             my_country=country,
                                             location=location,
                                             add_house_number=tags.get('addr:housenumber', ''),
                                             add_street=tags.get('addr:street', ''),
                                             add_postcode=tags.get('addr:postcode', ''),
                                             add_city=tags.get('addr:city', ''),
                                             add_country=tags.get('addr:country', ''),
                                             website=make_website(tags.get('website', '')),
                                             OSM_ID=osmid,
                                             OSM_storetype=o,
                                             lat=latitude,
                                             lon=longitude,
                                             )
                                    s.save()
                                    i += 1

                                except IntegrityError:
                                    s = Store.objects.get(OSM_ID=osmid)
                                    s.name = store_name
                                    s.location = location
                                    s.website = make_website(tags.get('website', ''))
                                    s.add_house_number = tags.get('addr:housenumber', '')
                                    s.add_street = tags.get('addr:street', '')
                                    s.add_postcode = tags.get('addr:postcode', '')
                                    s.add_city = tags.get('addr:city', '')
                                    s.add_country = tags.get('addr:country', '')
                                    s.OSM_storetype = o
                                    
                                    if not s.my_address:
                                        s.my_address = address

                                    s.lat = latitude
                                    s.lon = longitude

                                    s.save()
                                    
                                    skipped += 1
                                except DataError:
                                    logfile.write('Problem with', obj + '\n')

                        except KeyError:
                            pass
                logfile.write('    ' + str(i) + ' new stores loaded, ' + str(skipped) + ' stores updated\n')
                logfile.write('\n')


        # https://www.nationsonline.org/oneworld/country_code_list.htm
        country_list = {
            'Croatia': 'HR',
            'Great Britain': 'GB',
            'New Zealand': 'NZ',
            'Ireland': 'IE',
            'South Africa': 'ZA',
            'Canada': 'CA',
            'Jamaica': 'JM',
            'Germany': 'DE',
            'United States': 'US',
            'Norway': 'NO',
            'Sweden': 'SE',
            'Finland': 'FI',
            'Australia': 'AU',
            'Pakistan': 'PK',
            'Spain': 'ES',
            'France': 'FR', 
            'Switzerland': 'CH',
            'Denmark': 'DK',
            'Latvia': 'LV',
            'Lithuania': 'LT',
            'Estonia': 'EE',
            'Greece': 'GR',
            'Italy': 'IT'
        }

        #get latest from OSM
        #https://wiki.openstreetmap.org/wiki/Map_Features#Shop
        
        osm_shops = ['butcher', 'deli', 'cheese', 'dairy', 'farm', 'coffee', 'greengrocer', 'tea', 'spices']

        #delete_data()

        #MAIN PART OF ROUTINE

        #Delete all logfiles older than x days
        now = time.time()
        for old_logfile in os.listdir(LOGS_FOLDER):
            old_logfile = join(LOGS_FOLDER, old_logfile)
            days = 7
            
            if os.stat(old_logfile).st_mtime < now - days * 24 * 60 * 60:
                os.remove(old_logfile)

        #create new logfile and name
        load_start_time = dt.datetime.now()
        logfile_path = join(LOGS_FOLDER, load_start_time.strftime("%Y-%m-%d_%H-%M-%S"))
        logfile = open(logfile_path, "w")

        #Check number of records in store table - is this a first time load?
        #if yes, then force a load from any existing tables
        existing_count = Store.objects.count()
    
        country_count = len(country_list)
        i = 0

        for k, v in country_list.items():
            i += 1
            was_updated = get_data_from_OSM(k, v, osm_shops, fresh=False, max_days=2)
            if existing_count > 1: # already records exist
                if was_updated: # and we got new data
                   load_data(k, v, logfile)
            else:   # no records exist
                load_data(k, v, logfile) # do a load regardless

            #Uncomment to force a load during testing
            #load_data(k, v)

            if was_updated and i != country_count:
                logfile.write('    Waiting a bit before I do the next one...\n')
                logfile.write('\n')
                time.sleep(60)

        load_end_time = dt.datetime.now()
        logfile.write('Load start    ' + str(load_start_time) + '\n')
        logfile.write('Load end      ' + str(load_end_time) + '\n') 
        logfile.write('Load duration ' + str(load_end_time-load_start_time) + '\n')    

        logfile.close()

        print('Loading finished, check log to see results in:', logfile_path)



