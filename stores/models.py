#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils.encoding import escape_uri_path

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
    name = models.CharField(max_length=100)
    location = models.PointField()
    lat = models.FloatField()
    lon = models.FloatField()
    add_house_number = models.CharField(max_length=100)
    add_street = models.CharField(max_length=100)
    add_postcode = models.CharField(max_length=20)
    add_city = models.CharField(max_length=100)
    add_country = models.CharField(max_length=20)
    email = models.EmailField()

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
        return self.name

    def get_absolute_url(self):
        return reverse('store:store_profile', kwargs={'store_id': self.pk})

    def total_likes(self):
        return self.likes.count()

    def search_url(self):
        return  'https://www.google.com/maps/search/?api=1&query=' + str(self.lat) + ',' + str(self.lon)
        #return  'https://www.google.com/maps/search/?api=1&query=' + escape_uri_path(self.name) + '@' + str(self.lat) + ',' + str(self.lon)


class StoreComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='store_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

