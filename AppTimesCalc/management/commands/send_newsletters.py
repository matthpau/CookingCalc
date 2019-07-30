# this is to run daily and calculate and prepare the newsletters and recipients

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command

from django.db.models import Count

from users.models import CustomUser, Profile, Country
from stores.models import Store, Event

from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
    import datetime as dt

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.core import mail


# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):

        messages = []

        #Calculate action start date, assumed next Wednesday
        date = dt.date.today()
        day = 2 # Issue Day Wednesday (Monday is 0)

        #https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date
        onDay = lambda date, day: date + dt.timedelta(days=(day-date.weekday()+7)%7)
        next_newsletter_date = onDay(date, day)

        if next_newsletter_date == date:
            next_newsletter_date += dt.timedelta(days=7)
        
        next1_newsletter_date = next_newsletter_date + dt.timedelta(days=7)

        print(next_newsletter_date, next1_newsletter_date)
        #All users who want to get a newsletter in countries where we have a newsletter
        profiles = Profile.objects.filter(local_offer_receive=True).filter(add_country__run_newsletter=True)
        print(profiles)
      
        #Ignore those with invalid addresses
        profiles = profiles.filter(found_location__isnull=False)

        #print('XXX', profiles.values())
        
        for profile in profiles:
            #print('YYY', profile)
            user_location = profile.found_location
            search_dis = profile.local_offer_radius
            print(profile.user_id, user_location, profile.user.email)
            #print()

            stores = Store.objects.filter(location__distance_lte=(user_location, D(km=search_dis))) \
                    .annotate(num_events=Count('event')) \
                    .annotate(distance=Distance('location', user_location))

            stores = stores.filter(num_events__gt=0)

            
            #TODO is there a way to calculate it more efficiently and pick up distance from the stores query?
            events = Event.objects.all()
            events = events.filter(store__in=stores).annotate(distance=Distance('store__location', user_location)).order_by('-distance')

            #Only get those events that start or end in the period
            # Those that start in the period
            # Those that end in the period
            # Those that span the period
            events = events.filter(start_date__gte=next_newsletter_date, start_date__lte=next1_newsletter_date) | \
                events.filter(end_date__gte=next_newsletter_date, end_date__lte=next1_newsletter_date) | \
                events.filter(start_date__lte=next_newsletter_date, end_date__gte=next1_newsletter_date) 

            #For testing
            for e in events:
                print(e.id, e.store, e.start_date, e.end_date, e.includes_offers)

            context = {
                'profile': profile,
                'events': events,
                'search_dis': str(round(search_dis, 1)) + ' km'
                }

            msg_html = render_to_string('newsletters/weekly_general.html', context)

            #Writing to file for testing
            write_file = f'newsletters/testing/test-{str(profile.id)}.html' 
            with open(write_file, 'w') as f:
                f.write(msg_html)
            
            subject, from_email, to = 'your weekly cooking-helpers.com events', settings.DEFAULT_FROM_EMAIL, 'matthpau@gmail.com'
            text_content = 'This is an important message.'
            html_content = msg_html
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")

            messages.append(msg)

        connection = mail.get_connection()
        connection.send_messages(messages) 
