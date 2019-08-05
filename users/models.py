from django.contrib.auth.models import AbstractUser, UserManager
#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
#from stores.models import Country
from .businessLogic import nice_address
from django.utils.translation import gettext_lazy as _

# https://wsvincent.com/django-custom-user-model-tutorial/
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#substituting-a-custom-user-model
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

class CustomUserManager(UserManager):
    pass

class Country(models.Model):
    code=models.CharField(max_length=3, primary_key=True)
    name=models.CharField(_('Country'), max_length=50)
    run_newsletter=models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _('Country')
        
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    # add additional fields in here

    def __str__(self):
        return self.email


class Profile(models.Model):

    newsletter_language_choices = (
        ('EN', _("English")),
        ('DE', _("German")),
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    found_location = models.PointField(null=True, blank=True)
    found_address = models.CharField(_('Confirmed address'), max_length=500, null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)
    house_number = models.CharField(_('House Number'), max_length=10, default='', blank=True)
    street = models.CharField(_('Street'), max_length=100, default='', blank=True)
    add_2 = models.CharField(_('Address 2'), max_length=100, default='', blank=True)
    add_3 = models.CharField(_('Address 3'), max_length=100, default='', blank=True)
    add_postcode = models.CharField(_('Postcode'), max_length=20, default='', blank=True)
    add_city = models.CharField(max_length=100, default='', verbose_name=_('City'), blank=True)
    add_country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL, verbose_name=_('Country'), blank=True)
    local_offer_receive = models.BooleanField(_("I would like to receive the weekly local offers newsletter"), default=False)
    local_offer_radius = models.FloatField(_("Search radius for local offers (km)"), default=5, blank=True)
    newsletter_language = models.CharField(_("Newsletter Language"), max_length=2, choices=newsletter_language_choices, default='EN')

    def __str__(self):
        return str(self.id) + ' ' + str(self.user)

    @property
    def auto_address(self):
        return nice_address(self.add_1, self.add_2, self.add_3, self.add_city, str(self.add_country))

    @property
    def valid_address(self):
        return bool(nice_address)