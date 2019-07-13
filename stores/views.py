import json
from django.shortcuts import get_object_or_404, render
from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from .forms import StoreSearch
from .models import Store, StoreType
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.template.loader import render_to_string

def store_profile(request, store_id):
    my_store = get_object_or_404(Store, pk=store_id)

    is_liked = False
    if my_store.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {
        'store': my_store,
        'is_liked': is_liked,
        'store_id': store_id,
        'total_likes': my_store.total_likes(),
        }

    return render(request, 'stores/profile.html', context)


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
    lat, lon = g.lat_lon(found_ip)

    # Have a bit of fun
    #lat, lon, city['city'], city['country_name'] = 51.5074, 0.1278, 'London', 'UK'
    #lat, lon, city['city'], city['country_name'] = 43.6532, -79.3832, 'Toronto', 'Canada'
    #lat, lon, city['city'], city['country_name'] = 48.8566, 2.3522, 'Paris', 'France'
    #lat, lon, city['city'], city['country_name'] = 53.3498, -6.2603, 'Dublin', 'Ireland'

    user_location = Point(lon, lat, srid=4326)

    
    #Filter stores by distance
    results = Store.objects.annotate(distance=Distance('location', user_location))
    results = results.order_by('distance')[:100]

    context = {'city': city['city'],
               'country': city['country_name'],
               'store_list': results}

    return render(request, 'stores/search_results.html', context)


def get_loc(request):
    form = StoreSearch
    context = {'form': form}
    return render(request, 'stores/get_loc.html', context)


def process_loc(request):
    lat = float(request.GET.get('lat'))
    lon = float(request.GET.get('lon'))
    search_dis = request.GET.get('search_distance')
    sort_order = int(request.GET.get('sort_order'))
    store_filter = request.GET.get('store_filter')

    print('store_filter', store_filter)

    user_location = Point(lon, lat, srid=4326)

    #https://stackoverflow.com/questions/19703975/django-sort-by-distance
    #https://docs.djangoproject.com/en/2.2/ref/contrib/gis/db-api/
    #Filter stores by distance
    store_results = Store.objects.filter(location__distance_lte=(user_location, D(km=search_dis))) \
                    .annotate(distance=Distance('location', user_location)) \
                    .annotate(likes_total=Count('likes', distinct=True)) \
                    
    if sort_order == 1: #Distance
        store_results = store_results.order_by('distance')
    elif sort_order == 2: #Likes
       store_results = store_results.order_by('-likes_total')

    if store_filter:

        store_results = store_results.filter(OSM_storetype_id=store_filter)
  
    store_results = store_results.values()

    # since this is a dictionary with location (non serializable) and a calculated Distance, I
    # need to convert it the long way to a dictionary
    return_data = []
    for store in store_results:

        ww_dict = {}
        for key, val in store.items():
            if key == 'distance':
                ww_dict['distance'] = round(float(val.km), 1)  # convert the distance object to km
            elif key == 'location':
                pass
            elif key == 'OSM_storetype_id':
                ww_dict['icon_text'] = StoreType.objects.values().get(pk=val)['icon_text']
            else:
                ww_dict[key] = val

        # Create a google maps friendly search
        search_url = '&query=' + str(store['lat']) + ',' + str(store['lon'])
        ww_dict['search_url'] = search_url

        # Create a friendly address
        result = store['add_house_number'] + ' ' + store['add_street'] + ' ' + store['add_city'] + ' ' + store['add_country']
        result = result.replace('unknown', '')
        result = result.lstrip().rstrip()
            
        ww_dict['friendly_address'] = result
        
        return_data.append(ww_dict)

    return JsonResponse(return_data, safe=False)

@login_required
def store_like(request):
    store_id = int(request.POST.get('id_like'))
    my_store = get_object_or_404(Store, id=store_id)

    if my_store.likes.filter(id=request.user.id).exists():
        my_store.likes.remove(request.user)
        is_liked = False
    else:
        my_store.likes.add(request.user)
        is_liked = True

    context = {
        'is_liked': is_liked,
        'total_likes': my_store.total_likes(),
        'store_id': store_id
        }

    print('ajax', request.is_ajax())

    if request.is_ajax():
        html = render_to_string('stores/like_section.html', context, request=request)
        return JsonResponse({'form': html})
