from django.shortcuts import get_object_or_404, render
from .models import Store
from django.views.generic import CreateView, ListView
from geopy.geocoders import Nominatim
import json


class StoreCreate(CreateView):
    model = Store
    fields = ['name', 'address', 'store_url', 'tags']
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
    context_object_name = 'store_list_view'   #note defaults to object_list



