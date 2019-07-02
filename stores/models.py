#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.urls import reverse

# https://realpython.com/location-based-app-with-geodjango-tutorial/


class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    lat = models.FloatField()
    long = models.FloatField()
    address = models.CharField(max_length=200)
    add_house_number = models.CharField(max_length=100)
    add_street = models.CharField(max_length=100)
    add_postcode = models.CharField(max_length=20)
    add_city = models.CharField(max_length=50)
    add_country = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    opening_hours = models.CharField(max_length=200)
    website = models.CharField(max_length=50)
    OSM_ID = models.BigIntegerField(unique=True)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='stores')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)

    @property
    def addr_full(self):
        result = self.add_house_number + ' ' + self.add_street + ' ' + self.add_city + ' ' + self.add_country
        result = result.replace('unknown', '')
        result = result.lstrip().rstrip()

        if len(result) > 0:
            if result[-1] == ',':
                result = result[:-1]
        else:
            result = ''
        return result

    @property
    def url_search(self):
        return self.addr_full.replace(' ', '+')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:store_profile', kwargs={'store_id': self.pk})


class StoreComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='store_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


