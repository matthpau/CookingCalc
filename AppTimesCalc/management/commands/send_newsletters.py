# this is to run daily and calculate and prepare the newsletters and recipients

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command

from django.db.models import Count

from users.models import CustomUser, Profile, Country
from stores.models import Store, Event

from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
import datetime

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):
         
        #Calculate action start date, assumed next Wednesday
        date = datetime.date.today()
        day = 2 #Wednesday (Monday is 0)

        
        
        #https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date
        onDay = lambda date, day: date + datetime.timedelta(days=(day-date.weekday()+7)%7)
        
        next_newsletter_date = onDay(date, day)

        if next_newsletter_date == date:
            next_newsletter_date += datetime.timedelta(days=7)

        print(next_newsletter_date)
        #TODO YOU ARE HERE


        #All users who want to get a newsletter in countries where we have a newsletter
        profiles = Profile.objects.filter(local_offer_receive=True).filter(add_country__run_newsletter=True)
      
        #Ignore those with invalid addresses
        profiles = profiles.filter(found_location__isnull=False)

        #for testing 
        #TODO remove this if still here
        profiles = profiles.filter(id=5)

        #print(profiles.values())
        
        for profile in profiles:
            user_location = profile.found_location
            search_dis = profile.local_offer_radius
            #print(profile.user_id, user_location)
            print()

            stores = Store.objects.filter(location__distance_lte=(user_location, D(km=search_dis))) \
                    .annotate(num_events=Count('event')) \
                    .annotate(distance=Distance('location', user_location))

            stores = stores.filter(num_events__gt=0)
            #print(stores)
            print()
            
            events = Event.objects.filter(store__in=stores)
            print(events)
        

     