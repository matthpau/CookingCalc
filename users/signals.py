#from django.contrib.auth.models import User  # Standard User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        #equivalent to a = Profile(user=instance), a.save()

# Prevent recursion
# https://stackoverflow.com/questions/10840030/django-post-save-preventing-recursion-without-overriding-model-save


@receiver(post_save, sender=Profile)
def update_geo_info(sender, instance, created, **kwargs):
    if not instance:
        return

    if hasattr(instance, '_dirty'):
        return

    from django.contrib.gis.geos import fromstr
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="CookingCalc")
    my_loc = geolocator.geocode(instance.found_address)
    if my_loc:
        
        lat, lon = (my_loc.latitude, my_loc.longitude)
        location = fromstr(f'POINT({lon} {lat})', srid=4326)
        
        instance.lat = lat
        instance.lon = lon
        instance.found_location = location

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty
    