from django.shortcuts import get_object_or_404, render
from .models import Store
from django.views.generic import CreateView, ListView
from geopy.geocoders import Nominatim
import json
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.http import HttpResponse, JsonResponse
from .forms import StoreSearch

class StoreCreate(CreateView):
    model = Store
    fields = ['name', 'address', 'tags']
    success_url = '/stores/list'
    # points to store_form.html automatically

    def form_valid(self, form):
        geolocator = Nominatim(user_agent="CookingHelpers")
        location = geolocator.geocode(form.instance.address, addressdetails=True)
        print(location.raw)
        print(location.raw['address'])

        if location:
            form.instance.cl_latitude = location.latitude
            form.instance.cl_longitude = location.longitude
            if location.raw['address'].get('city', None):
                form.instance.cl_city = location.raw['address']['city']
            elif location.raw['address'].get('city_district', None):
                form.instance.cl_city = location.raw['address']['city_district']
            else:
                form.instance.cl_city = 'check city'

            #form.instance.cl_city = location.raw['address']['city']
            form.instance.cl_country_code = location.raw['address']['country_code']
            form.instance.cl_country = location.raw['address']['country']
            form.instance.cl_postcode = location.raw['address']['postcode']
            form.instance.cl_state = location.raw['address']['state']
            form.instance.cl_address = json.dumps(location.raw['address'])

        return super().form_valid(form)


def store_profile(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    context = {'store': store}
    return render(request, 'stores/profile.html', context)


class StoreList(ListView):
    model = Store
    context_object_name = 'store_list_view'   #note context defaults to object_list

def store_search(request):
    # https://docs.djangoproject.com/en/2.2/ref/contrib/gis/geoip2/#
    # https://github.com/un33k/django-ipware
    # https://developers.google.com/maps/documentation/urls/guide

    #dev_ip = 'www.hamburg.de'  # for use during development, Hamburg Germany
    dev_ip = '2a02:8108:4640:1214:b9e5:9090:525c:d282'
    #Get client ip address
    client_ip, is_routable = get_client_ip(request)

    if client_ip is None:
        found_ip = dev_ip
    else:
        # We got the client's IP address
        if is_routable:
            found_ip = client_ip
        else:
            #found_ip = 'Your IP is private'
            found_ip = dev_ip

    # Get location from IP address
    g = GeoIP2()
    city = g.city(found_ip)
    print(city)
    lat, lon = g.lat_lon(found_ip)

    # Have a bit of fun
    #lat, lon, city['city'], city['country_name'] = 51.5074, 0.1278, 'London', 'UK'
    #lat, lon, city['city'], city['country_name'] = 43.6532, -79.3832, 'Toronto', 'Canada'
    #lat, lon, city['city'], city['country_name'] = 48.8566, 2.3522, 'Paris', 'France'
    #lat, lon, city['city'], city['country_name'] = 53.3498, -6.2603, 'Dublin', 'Ireland'

    user_location = Point(lon, lat, srid=4326)

    #Filter stores by distance
    q = Store.objects.annotate(distance=Distance('location', user_location))
    q = q.order_by('distance')[:100]

    context = {'city': city['city'],
               'country': city['country_name'],
               'store_list': q}

    return render(request, 'stores/search_results.html', context)


def get_loc(request):
    form = StoreSearch
    context = {'form': form}
    return render(request, 'stores/get_loc.html', context)


def process_loc(request):
    lat = float(request.GET.get('lat'))
    lon = float(request.GET.get('lon'))
    print(request.GET)

    user_location = Point(lon, lat, srid=4326)

    #Filter stores by distance
    store_results = Store.objects.annotate(distance=Distance('location', user_location))
    store_results = store_results.order_by('distance')[:20].values()
    # since this is a dictionary with location (non serializable) and a calculated Distance, I 
    # need to convert it the long way to a dictionary
    return_data = []
    for store in store_results:
        ww_dict = {}
        for key, val in store.items():
            if key == 'distance':
                ww_dict['distance'] = float(val.km)  # convert the distance object to km
            elif key == 'location':
                pass
            else:
                ww_dict[key] = val
        return_data.append(ww_dict)

    # mydict = {'you': 1, 'did': 2, 'it':3}
    # do other stuff to enhance the context
    return JsonResponse(return_data, safe=False)






