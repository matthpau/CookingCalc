# this is to run daily and calculate and prepare the newsletters and recipients

import datetime as dt
import random

from django.core.management.base import BaseCommand
from django.conf import settings
#from django.core.management import call_command

from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

from django.db.models import Count

from users.models import Profile, CustomUser
from stores.models import Store, Event

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

from django.core import mail
from django.contrib.sites.models import Site
from django.utils import translation

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0


class Command(BaseCommand):

    def handle(self, *args, **options):

        def newsletter_prep(desired_send_day):
            """
            desired_send_day = integer representing day of the week to send the newsletter. 0 is Monday.
            returns:
            next_newsletter_date effective start period newsletter
            next1_newsletter_date effective end period newsletter
            """

            today = dt.date.today()
            today_day_of_week = today.weekday()

            # https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date
            def on_day(date, desired_send_day): return today + \
                dt.timedelta(days=(desired_send_day-date.weekday()+7) % 7)
            # onday calculates the next effective newsletter day

            next_newsletter_date = on_day(today, desired_send_day)
            next1_newsletter_date = next_newsletter_date + dt.timedelta(days=6)
            # Are we sending the newsletter today?
            send_flag = desired_send_day == today_day_of_week

            return send_flag, next_newsletter_date, next1_newsletter_date

        def send_newsletters(next_newsletter_date, next1_newsletter_date):

            cur_language = translation.get_language()

            messages = []
            # All users who want to get a newsletter in countries where we have a newsletter
            profiles = Profile.objects.filter(local_offer_receive=True).filter(
                add_country__run_newsletter=True)

            # Ignore those with invalid addresses
            profiles = profiles.filter(found_location__isnull=False)

            for profile in profiles:

                user_location = profile.found_location
                search_dis = profile.local_offer_radius
                dest_email = profile.user.email
                print(dest_email)

                language = profile.newsletter_language
                translation.activate(language)

                stores = Store.objects.filter(location__distance_lte=(user_location, D(km=search_dis))) \
                    .annotate(num_events=Count('event')) \
                    .annotate(distance=Distance('location', user_location))

                stores = stores.filter(num_events__gt=0)

                # TODO is there a way to calculate it more efficiently and pick up distance from the stores query?
                events = Event.objects.all()
                events = events.filter(store__in=stores).annotate(
                    distance=Distance('store__location', user_location)).order_by('distance')

                # Only get those events that start or end in the period
                # Those that start in the period
                # Those that end in the period
                # Those that span the period
                events = events.filter(start_date__gte=next_newsletter_date, start_date__lte=next1_newsletter_date) | \
                    events.filter(end_date__gte=next_newsletter_date, end_date__lte=next1_newsletter_date) | \
                    events.filter(start_date__lte=next_newsletter_date,
                                  end_date__gte=next1_newsletter_date)

                base_url = str(Site.objects.get_current())

                # print(Site.objects.get_current())
                # print(Site.objects.get_current().domain)

                context = {
                    'profile': profile,
                    'events': events,
                    'search_dis': str(round(search_dis, 1)) + ' km',
                    'base_url': base_url,
                    'profile_url': base_url + "/users/profile"
                }

                msg_html = render_to_string(
                    'newsletters/weekly_general.html', context)

                now = dt.datetime.now().strftime('%a, %d %B')

                # Writing to file for testing
                """
                print(now)
                write_file = f'newsletters/testing/test-{dest_email}-{now}.html'
                with open(write_file, 'w') as f:
                    f.write(msg_html)
                """

                subject = 'Your weekly cooking-helpers.com news -    ' + now
                from_email = settings.DEFAULT_FROM_EMAIL
                to = dest_email
                text_content = 'This is an important message.'
                html_content = msg_html
                msg = EmailMultiAlternatives(
                    subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")

                messages.append(msg)

            connection = mail.get_connection()
            connection.send_messages(messages)

            # Revert to language before the routine was called
            translation.activate(cur_language)

        def newsletters_main(desired_send_day):
            #0 is monday
            send_flag, start_date, end_date = newsletter_prep(desired_send_day)

            if send_flag:
                send_newsletters(start_date, end_date)
                return 'Newsletters sent'
            else:
                return 'Newsletters not sent, wrong day'

        from django.conf import settings
        #print(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print(newsletters_main(6))  # run the whole process. 0 is Monday
