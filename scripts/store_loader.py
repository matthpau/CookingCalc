"""
adapted from https://realpython.com/location-based-app-with-geodjango-tutorial/#displaying-nearby-shops
to load data from https://overpass-turbo.eu/
download format download/copy as raw OSM data
"""
import django
import json
import os
from django.contrib.gis.geos import fromstr
from django.apps import apps
from django.db.utils import IntegrityError
from geopy.geocoders import Nominatim

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CookingBase.settings")
django.setup()

from stores.models import Store

DATA_PATH = '../dumps/store_import/'


def delete_data():
    Store.objects.all().delete()


def load_data(filename):
    geolocator = Nominatim(user_agent="cookingcalc")
    i = 0
    Shop = apps.get_model('stores', 'Store')
    jsonfile = DATA_PATH + filename

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
                        #store already exists, has OSM_ID in database
                        pass
            except KeyError:
                pass
    print(i, 'stores loaded')


print('clearing table')
delete_data()
print('loading table')
load_data('germany.json')
