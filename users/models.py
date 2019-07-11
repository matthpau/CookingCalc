from django.contrib.auth.models import AbstractUser, UserManager
#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
#from stores.models import Country


# https://wsvincent.com/django-custom-user-model-tutorial/
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

class CustomUserManager(UserManager):
    pass


class Country(models.Model):
    code=models.CharField(max_length=3, primary_key=True)
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    # add additional fields in here

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.PointField(null=True)
    birth_date = models.DateField(null=True, blank=True)
    add_1 = models.CharField(max_length=100, default='', verbose_name='Address 1')
    add_2 = models.CharField(max_length=100, default='', verbose_name='Address 2', blank=True)
    add_3 = models.CharField(max_length=100, default='', verbose_name='Address 3', blank=True)
    add_postcode = models.CharField(max_length=20, default='', blank=True, verbose_name='Postcode')
    add_city = models.CharField(max_length=100, default='', verbose_name='City')
    add_country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL, verbose_name='Postcode')

    local_offer_receive = models.BooleanField(default=False, verbose_name="Do you want to receive newsletters with local offers?")
    local_offer_radius = models.FloatField(default=5, verbose_name="Search radius for local offers (km)")

    def __str__(self):
        return str(self.user)

    def nice_address(self):
        result = ', '.join([self.add_1, self.add_2, self.add_3, self.add_city, self.add_country]) 
        # Get rid of any double or triple commas
        char = ", "
        pattern = '(' + char + '){2,}'
        result = re.sub(pattern, char, result)

        return result