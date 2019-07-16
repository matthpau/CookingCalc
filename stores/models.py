#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from taggit.managers import TaggableManager
from bootstrap_datepicker_plus import DateTimePickerInput
from bootstrap_datepicker_plus import DateTimePickerInput


# https://realpython.com/location-based-app-with-geodjango-tutorial/

class Country(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50, default='please complete country')

    def __str__(self):
        return self.code + ' ' + self.name

class StoreType(models.Model):
    type_text = models.CharField(max_length=50, primary_key=True)
    icon_text = models.CharField(max_length=50)

    def __str__(self):
        return self.type_text

class Store(models.Model):
    """
    basic store model
    """
    name = models.CharField(max_length=100)
    location = models.PointField()
    lat = models.FloatField()
    lon = models.FloatField()
    add_house_number = models.CharField(_('House Number'), max_length=100)
    add_street = models.CharField(_('Street'), max_length=100)
    add_postcode = models.CharField(_('Postcode'), max_length=100)
    add_city = models.CharField(_('City'), max_length=100)
    add_country = models.CharField(_('Country'), max_length=20)
    email = models.EmailField()

    authorised_editors = models.ManyToManyField(get_user_model(), through='AuthorisedEventEditors', related_name="authorised_editors")

    my_name = models.CharField(max_length=100)
    my_address = models.CharField(max_length=300)
    my_country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

    phone = models.CharField(max_length=50)
    opening_hours = models.CharField(max_length=200)
    website = models.TextField(null=True)
    OSM_ID = models.BigIntegerField(unique=True)
    OSM_storetype = models.ForeignKey(StoreType, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='store_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return str(self.id) + ' ' + self.name

    def get_absolute_url(self):
        return reverse('store:store_profile', kwargs={'store_id': self.pk})

    def total_likes(self):
        return self.likes.count()

    def search_url(self):
        return  'https://www.google.com/maps/search/?api=1&query=' + str(self.lat) + ',' + str(self.lon)

    def events_url(self):
        return  reverse('store:eventslist', kwargs={'store_id': self.pk})


class AuthorisedEventEditors(models.Model):
    """
    List of users who can edit events for this store
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)  + ' / ' + str(self.store) + ' / ' + str(self.user)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['store', 'user'], name='Uniqueperstore'),
        ]    


class StoreComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='store_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event(models.Model):
    """
    Events (promotions etc per store)
    """

    datetime_format = "%d / %m / %Y %H:%M"

    created_by_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=100)
    comment = models.TextField(_('Event description'))
    start_date = models.DateTimeField(_('Event start date and time'))
    end_date = models.DateTimeField(_('Event end date and time'))
    includes_offers = models.BooleanField(_('Includes offers'), default=False)
    archived = models.BooleanField(_('Archived'), default=False)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    def __str__(self):
        return str(self.id) + ' ' + self.title + ' | ' + str(self.start_date) + ' ' + str(self.start_date)
