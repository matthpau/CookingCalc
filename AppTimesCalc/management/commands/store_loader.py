# this is run to provide some initial values for which the database works


from django.core.management.base import BaseCommand
from django.conf import settings
import requests

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):
        import json
        from os.path import isfile, join
        import os
        import datetime as dt
        import time
        from django.contrib.gis.geos import fromstr
        from django.apps import apps
        from django.db.utils import DataError
        from stores.models import Store, StoreType, Country

        DUMP_FOLDER = 'dumps/store_import'
        LOG_FOLDER = 'logs/store_load'

        def delete_data():
            print('clearing all records')
            Store.objects.all().delete()
            print('all records have been deleted')
            print()

        #https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
        def get_data_from_OSM(country_name_no_sp, country_code, osm_shops, logfile, save_file, fresh=False, max_days=2):

            """
            fresh True forces a download regardless of file age
            maxAge in days how old a file should be before being replaced
            """
            was_replaced = False
            
            if fresh:
                max_file_age = 0
            else:   
                max_file_age = max_days * 24 * 60 * 60  #how old a file needs to be before it is replace, secs
            
            logfile.write('Getting data for ' + country_name_no_sp + ' using savefile: ' + save_file + '\n')

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
                    logfile.write('File still up to date, keeping existing, no update this run\n')
            else:
                replace_flag = True

            if replace_flag:
                logfile.write('File out of date, getting update from OSM\n')
                r = requests.get(overpass_url, params={'data': overpass_query})

                if r.status_code == 200:
                    #Write OSM data to file
                    with open(save_file, 'w') as f:
                        json.dump(r.json(), f)
                        logfile.write('Local save complete\n')
                        was_replaced = True
                else:
                    #Report errors
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

        def load_data(country_name_no_sp, country_code, logfile, save_file):
            nice_name = country_name_no_sp.replace('_', ' ')

            #Add country to list of countries if not there
            country, created = Country.objects.get_or_create(
                pk=country_code,
                defaults={'name':nice_name}
                )

            if save_file:
                new_count = 0
                updated_count = 0

                shop = apps.get_model('stores', 'Store')

                #Import file
                with open(str(save_file)) as datafile:
                    objects = json.load(datafile)
                    for obj in objects['elements']:
                        obj_type = obj['type']
                        if obj_type == 'node':
                            osmid = obj.get('id', 0)

                            #Prepare the data for loading or updating
                            
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

                                store_type = StoreType.objects.get(pk=tags.get('shop', ''))

                                #Check if OSMID exists already in database
                                search_store = Store.objects.filter(OSM_ID=osmid)

                                if search_store.exists():
                                    #Store exists in database, do the update routine
                                    found_store = search_store.first()

                                    found_store.name = store_name
                                    found_store.location = location
                                    found_store.website = make_website(tags.get('website', ''))
                                    found_store.add_house_number = tags.get('addr:housenumber', '')
                                    found_store.add_street = tags.get('addr:street', '')
                                    found_store.add_postcode = tags.get('addr:postcode', '')
                                    found_store.add_city = tags.get('addr:city', '')
                                    found_store.add_country = tags.get('addr:country', '')
                                    found_store.OSM_storetype = store_type
                                    found_store.lat = latitude
                                    found_store.lon = longitude
                                    
                                    found_store.save()
                                    updated_count += 1
                                
                                else:
                                    #New store
                                    new_store = shop(name=store_name,
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
                                             OSM_storetype=store_type,
                                             lat=latitude,
                                             lon=longitude,
                                             )
                                    new_store.save()
                                    new_count += 1

                logfile.write('    ' + str(new_count) + ' new stores, ' + str(updated_count) + ' stores updated\n')

        def store_load_main(country_list, osm_shops, log_folder, dump_folder, fresh):
            
            load_start_time = dt.datetime.now()
            logfile_name = load_start_time.strftime("%Y-%m-%d--%H-%M-%S")

            #Delete all logfiles older than x days
            now = time.time()
            for old_logfile in os.listdir(log_folder):
                old_logfile = join(log_folder, old_logfile)
                days = 7
                
                if os.stat(old_logfile).st_mtime < now - days * 24 * 60 * 60:
                    os.remove(old_logfile)

            #create new logfile and name
            log_file_full = join(log_folder, logfile_name)
            logfile = open(log_file_full, "w")

            if fresh:
                logfile.write('fresh=True option selected, forcing download of all data\n')
            else:
                logfile.write('fresh=False option selected, existing dumps will be kept\n')


            #Check number of records in store table - is this a first time load?
            #if yes, then force a load from any existing tables
            existing_count = Store.objects.count()

            country_count = len(country_list)
            i = 0

            for country_name, country_code in country_list.items():
                i += 1
                country_name_no_sp = country_name.replace(' ', '_').lower()
                save_file = join(dump_folder, country_name_no_sp + '.json')
                was_updated = get_data_from_OSM(country_name_no_sp, country_code, osm_shops, logfile, save_file, fresh=fresh, max_days=1)
                
                #If data not updated, no need to upload it

                to_load_flag = False
                if existing_count > 1: # already records exist
                    if was_updated: # and we got new data
                        to_load_flag = True
                else:   # no records exist
                    to_load_flag = True

                if to_load_flag:
                    load_data(country_name_no_sp, country_code, logfile, save_file)

                if was_updated and i != country_count:
                    logfile.write('    Waiting a bit before I do the next one...\n')
                    logfile.write('\n')
                    time.sleep(60)

            load_end_time = dt.datetime.now()
            logfile.write('Load start    ' + str(load_start_time) + '\n')
            logfile.write('Load end      ' + str(load_end_time) + '\n') 
            logfile.write('Load duration ' + str(load_end_time-load_start_time) + '\n')    
            logfile.close()

            print('Loading finished, check log to see results in:', log_file_full)
        
        print('Running the store loader')

        #Check which machine we are on 
        if os.path.exists(settings.BASE_DIR_PDN):   #We are on the production server
            base_dir = settings.BASE_DIR_PDN
            print('You are on on the production server')
        else:                                       #We are on the local dev machine
            base_dir = settings.BASE_DIR
            print('You are on on the local dev machine')

        log_folder = join(base_dir, LOG_FOLDER)
        dump_folder = join(base_dir, DUMP_FOLDER)
        
        #About makedirs https://stackoverflow.com/questions/13819496/what-is-different-between-makedirs-and-mkdir-of-os

        for folder in [log_folder, dump_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        #USER INPUT SECTION
        # https://www.nationsonline.org/oneworld/country_code_list.htm
        country_list = {
            #'Croatia': 'HR',
            'Great Britain': 'GB',
            'New Zealand': 'NZ',
            'Ireland': 'IE',
            #'South Africa': 'ZA',
            #'Canada': 'CA',
            #'Jamaica': 'JM',
            'Germany': 'DE',
            #'United States': 'US',
            #'Norway': 'NO',
            #'Sweden': 'SE',
            #'Finland': 'FI',
            'Australia': 'AU',
            #'Pakistan': 'PK',
            #'Spain': 'ES',
            #'France': 'FR', 
            'Switzerland': 'CH',
            #'Denmark': 'DK',
            #'Latvia': 'LV',
            #'Lithuania': 'LT',
            #'Estonia': 'EE',
            #'Greece': 'GR',
            #'Italy': 'IT',
            #'Argentina': 'AR',
            #'Brazil': 'BR'
        }

        #get latest from OSM
        #https://wiki.openstreetmap.org/wiki/Map_Features#Shop
        
        osm_shops = [
            'butcher',
            'deli',
            'cheese',
            'dairy',
            'farm',
            'coffee',
            'greengrocer',
            'tea',
            'spices',
            'seafood',
            'fishmonger'
            ]

        store_load_main(country_list, osm_shops, log_folder, dump_folder, fresh=True)