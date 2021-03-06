from django.shortcuts import get_object_or_404, render

from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, When, Value, BooleanField, Case
from django.template.loader import render_to_string
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages

from datetime import datetime as dt, date

from .forms import StoreSearch
from .models import Store, StoreType
from users.models import CustomUser, Profile
from stores.models import Event, AuthorisedEventEditors as Editors
from .forms import EventAddCreate

from ipware import get_client_ip


def store_profile(request, store_id):
    my_store = get_object_or_404(Store, pk=store_id)

    is_liked = False
    if my_store.likes.filter(id=request.user.id).exists():
        is_liked = True

    # Get list of authorised event editors for this store
    store_editors = CustomUser.objects.filter(
        authorisedeventeditors__store__id=store_id)

    # Get count of events for display
    events_store = Event.objects.filter(store__id=store_id)
    events_all_count = events_store.count()

    now = dt.now()

    events_live = events_store.filter(start_date__lt=now, end_date__gt=now)
    events_upcoming_count = events_store.filter(end_date__gt=now).count()

    # Get count of editors for display
    editors_count = Editors.objects.filter(store__id=store_id).count()

    context = {
        'store': my_store,
        'is_liked': is_liked,
        'store_id': store_id,
        'total_likes': my_store.total_likes(),
        'editors': store_editors,
        'editors_count': editors_count,
        'all_count': events_all_count,
        'upcoming_count': events_upcoming_count,
        'events': events_live
    }

    return render(request, 'stores/profile.html', context)


def store_search(request):
    # https://docs.djangoproject.com/en/2.2/ref/contrib/gis/geoip2/#
    # https://github.com/un33k/django-ipware
    # https://developers.google.com/maps/documentation/urls/guide

    # dev_ip = 'www.hamburg.de'  # for use during development, Hamburg Germany
    dev_ip = '2a02:8108:4640:1214:b9e5:9090:525c:d282'
    # Get client ip address
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

    # Filter stores by distance
    results = Store.objects.annotate(
        distance=Distance('location', user_location))
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
    search_from = int(request.GET.get('search_from'))
    search_dis = request.GET.get('search_distance')
    sort_order = int(request.GET.get('sort_order'))
    store_filter = request.GET.get('store_filter')

    home_loc_fail = False

    if search_from == 1:  # selet from current location
        user_location = Point(lon, lat, srid=4326)
    elif search_from == 2:  # try and select from registered location, message if fail

        home_addr = Profile.objects.get(user=request.user).found_address
        if home_addr:
            user_location = Profile.objects.get(
                user=request.user).found_location

        else:
            user_location = Point(lon, lat, srid=4326)
            home_loc_fail = True

        # replace:

    # https://stackoverflow.com/questions/19703975/django-sort-by-distance
    # https://docs.djangoproject.com/en/2.2/ref/contrib/gis/db-api/
    # Filter stores by distance
    store_results = Store.objects.filter(location__distance_lte=(user_location, D(km=search_dis))) \
        .annotate(distance=Distance('location', user_location)) \
        .annotate(likes_total=Count('likes', distinct=True)) \

    if sort_order == 1:  # Distance
        store_results = store_results.order_by('distance')
    elif sort_order == 2:  # Likes
        store_results = store_results.order_by('-likes_total')

    if store_filter:
        store_results = store_results.filter(OSM_storetype_id=store_filter)

    # get any related events to show in the search screen. Do this for all stores shown, we will subfilter later
    live_events_all = Event.objects.filter(store__in=store_results)

    # show only events that are live right now
    today = dt.today()
    live_events_all = live_events_all.filter(
        start_date__lte=today, end_date__gte=today)

    store_results = store_results.values()
    # since this is a dictionary with location (non serializable) and a calculated Distance, I
    # need to convert it the long way to a dictionary
    return_data = []
    store_results = store_results.values()

    for store in store_results:

        ww_dict = {}
        for key, val in store.items():
            if key == 'distance':
                # convert the distance object to km
                ww_dict['distance'] = round(float(val.km), 1)
            elif key == 'location':
                pass
            elif key == 'OSM_storetype_id':
                ww_dict['icon_text'] = StoreType.objects.values().get(pk=val)[
                    'icon_text']
            else:
                ww_dict[key] = val

        # Create a google maps friendly search
        search_url = '&query=' + str(store['lat']) + ',' + str(store['lon'])
        ww_dict['search_url'] = search_url

        # Create a friendly address
        result = store['add_house_number'] + ' ' + store['add_street'] + \
            ' ' + store['add_city'] + ' ' + store['add_country']
        result = result.replace('unknown', '')
        result = result.lstrip().rstrip()

        ww_dict['friendly_address'] = result

        # Append Event Information
        live_events_store = live_events_all.filter(store__id=ww_dict['id'])

        if live_events_store.exists():

            events_dict = {}
            for event in live_events_store:
                event_detail = [
                    event.title,
                    event.comment,
                    str(event.end_date),
                    event.includes_offers
                ]
                events_dict[event.id] = event_detail
            ww_dict['events_count'] = live_events_store.count()
            ww_dict['events'] = events_dict
        else:
            ww_dict['events_count'] = 0
            ww_dict['events'] = {}

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

    if request.is_ajax():
        html = render_to_string(
            'stores/like_section.html', context, request=request)
        return JsonResponse({'form': html})

# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views


class EventsList(ListView):
    # template is automatically calculated as event_list.html
    model = Event
    context_object_name = 'events'

    def get_queryset(self):
        today = date.today()
        events_qs = Event.objects.filter(
            store__id=self.kwargs['store_id']).order_by('start_date')

        # https://docs.djangoproject.com/en/2.2/ref/models/conditional-expressions/
        # Add in a flag if the event is old
        events_qs = events_qs.annotate(
            old_event=Case(
                When(end_date__lt=today, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        return events_qs

    # https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # include context showing allowed editors, needs to be checked in order to show the view
        context['editors'] = CustomUser.objects.filter(
            authorisedeventeditors__store__id=self.kwargs['store_id'])
        context['store'] = Store.objects.get(pk=self.kwargs['store_id'])
        return context

# http://melardev.com/blog/2017/11/04/createview-django-4-examples/
# shows how to do extra processing before save

# https://docs.djangoproject.com/en/2.2/topics/auth/default/#limiting-access-to-logged-in-users-that-pass-a-test
# shows how to do a test on user before allowing permission (e.g. onlyusers from this store are allowed to create events)


class CreateEvent(UserPassesTestMixin, CreateView):

    model = Event
    # don't use BOTH fields and form_class, choose one or the other.
    # Fields are specified in the form_class
    # fields = ('title', 'comment', 'start_date', 'end_date', 'includes_offers')
    form_class = EventAddCreate

    # template_name  automatically is stores/event_form.html but we want to overwrite
    template_name = 'stores/event_create.html'

    def test_func(self):
        # returns true or false, depending if person is authorised editor for this store
        store_id = self.kwargs['store_id']
        store_editors = CustomUser.objects.filter(
            authorisedeventeditors__store__id=store_id)
        return self.request.user in store_editors

    def form_valid(self, form):
        model = form.save(commit=False)
        model.created_by_user = self.request.user
        model.store = Store.objects.get(id=self.kwargs['store_id'])
        model.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('store:eventslist', kwargs={'store_id': self.kwargs['store_id']})


class UpdateEvent(UserPassesTestMixin, UpdateView):
    form_class = EventAddCreate
    template_name = 'stores/event_update.html'

    def test_func(self):
        # returns true or false, depending if person is authorised editor for this event - store
        event_id = self.kwargs['event_id']
        event_editors = CustomUser.objects.filter(
            authorisedeventeditors__store__event__id=event_id)
        return self.request.user in event_editors

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs['event_id'])

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        event_id = self.kwargs['event_id']
        store_id = Store.objects.values().get(event__id=event_id)['id']
        return reverse('store:eventslist', kwargs={'store_id': store_id})


class DeleteEvent(UserPassesTestMixin, DeleteView):
    template_name = 'stores/event_delete.html'

    def test_func(self):
        # returns true or false, depending if person is authorised editor for this event - store
        event_id = self.kwargs['event_id']
        event_editors = CustomUser.objects.filter(
            authorisedeventeditors__store__event__id=event_id)
        return self.request.user in event_editors

    def get_object(self):
        event_id = self.kwargs.get('event_id')
        return get_object_or_404(Event, pk=event_id)

    def get_success_url(self):
        event_id = self.kwargs['event_id']
        store_id = Store.objects.values().get(event__id=event_id)['id']
        return reverse('store:eventslist', kwargs={'store_id': store_id})


def editors(request, store_id):
    store_name = Store.objects.get(pk=store_id).name

    context = {
        'store_id': store_id,
        'store_name': store_name
    }
    return render(request, 'stores/editors.html', context=context)


def editors_list(request, store_id):

    # Get list of authorised editors for this store
    # No need to check if empty. The users only sees this view if they are already an editor
    # They must be added manually first
    response = CustomUser.objects.filter(
        authorisedeventeditors__store__id=store_id)
    response = list(response.values())
    return JsonResponse(response, safe=False)


def store_launch_info(request):
    return render(request, 'stores/new_store_info.html')


def editor_delete(request):
    store_id = request.POST.get('del_store_id')
    user_id = request.POST.get('del_user_id')

    store_editors = CustomUser.objects.filter(
        authorisedeventeditors__store__id=store_id)

    if request.user in store_editors:
        delete_user = Editors.objects.filter(
            store_id=store_id, user_id=user_id)
        print(delete_user)
        delete_user.delete()

        return JsonResponse({
            'authorised': True,
            'response_text': _('User has been removed')
        })
    else:
        return JsonResponse({
            'authorised': False,
            'response_text': _('Not permitted')
        })


def editor_create(request):
    email = request.POST.get('email')
    store_id = request.POST.get('store_id')

    # Add a new user to authorised editors
    # get user first
    try:
        u = CustomUser.objects.get(email=email)

    except CustomUser.DoesNotExist:
        msg = {
            'status': 'not_found',
            'response_text': _('User not found, please ensure they create an account, or check your spelling')
        }

        return JsonResponse(msg)

    s = Store.objects.get(id=store_id)
    e, created = Editors.objects.get_or_create(
        store=s,
        user=u)
    msg = {
        'email': u.email,
        'id': u.id,
    }

    if created:
        msg['status'] = 'created'
        msg['response_text'] = _('User has been added to the list of editors')
    else:
        msg['status'] = 'exists'
        msg['response_text'] = _(
            'User is already in the list of editors, please check and try again')

    return JsonResponse(msg)
