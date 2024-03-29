from django.db import models
from django.contrib.auth import get_user_model
import datetime as dt
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

"""
https://docs.djangoproject.com/en/2.2/ref/models/options/
https://docs.djangoproject.com/en/2.2/ref/models/fields/
https://docs.djangoproject.com/en/2.2/ref/models/constraints/
https://docs.djangoproject.com/en/2.2/ref/models/relations/
https://docs.djangoproject.com/en/2.2/topics/db/queries/#lookups-that-span-relationships
"""


class MeatType(models.Model):
    MeatTypeName = models.CharField(max_length=60, unique=True)
    PortionKGPerAdult = models.FloatField(default=0)
    PortionKGPerChild = models.FloatField(default=0)

    def __str__(self):
        return self.MeatTypeName

    class Meta:
        ordering = ['MeatTypeName']


class CookingLevel(models.Model):
    CookingLevel = models.CharField(max_length=30, unique=True)
    CookingLevelSort = models.IntegerField()
    CookingInfo = models.ManyToManyField(MeatType, through='CookingInfo')

    def __str__(self):
        return self.CookingLevel

    class Meta:
        ordering = ['CookingLevelSort']


class CookingInfo(models.Model):
    MeatType = models.ForeignKey(MeatType, on_delete=models.CASCADE)
    CookingLevel = models.ForeignKey(CookingLevel, on_delete=models.CASCADE)
    NotRecommended = models.BooleanField(default=False)
    BrowningMins = models.IntegerField(default=0)
    BrowningTempC = models.IntegerField(default=0)
    OvenTempC = models.IntegerField(default=0)
    InternalTempC = models.IntegerField(default=0)
    MinsPerKg = models.IntegerField(default=0)
    MinsFixed = models.IntegerField(default=0)
    RestTimeMins = models.IntegerField(default=0)

    def __str__(self):
        return str(self.MeatType) + ' ' + str(self.CookingLevel)

    class Meta:
        verbose_name_plural = 'CookingInfo'
        ordering = ['MeatType', 'CookingLevel__CookingLevelSort']
        constraints = [
            models.UniqueConstraint(fields=['MeatType', 'CookingLevel'], name='UniquePerMeat'),
        ]
# https://wsvincent.com/django-referencing-the-user-model/


class MealPlan(models.Model):

    CookingOutcomes = (
        (1, _('Very undercooked')),
        (2, _('Undercooked')),
        (3, _('Just right')),
        (4, _('Overcooked')),
        (5, _('Very overcooked'))
    )

    Ratings = (
        (0, _('Not rated')),
        (1, _('One star')),
        (2, _('Two stars')),
        (3, _('Three stars'))
        )

    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    PlanName = models.CharField(max_length=100, verbose_name=_("Plan Name"))
    PlanDesc = models.TextField(blank=True, verbose_name=_("Plan Description"))
    MeatType = models.ForeignKey(MeatType, on_delete=models.CASCADE)  # MeatType
    CookingLevel = models.ForeignKey(CookingLevel, on_delete=models.CASCADE)  # CookingLevel

    StartTime = models.TimeField(default=dt.time(0, 0), verbose_name=_("Start Time"))  # StartTime
    MeatInTime = models.TimeField(default=dt.time(0, 0), verbose_name=_("Meat In Time"))  # MeatInTime
    RemoveTime = models.TimeField(default=dt.time(0, 0), verbose_name=_("Meat Out Time"))   # RemoveTime
    EatingTime = models.TimeField(default=dt.time(0, 0), verbose_name=_("Eating Time"))  # EatingTime

    WarmupTime = models.DurationField(default=dt.timedelta(0), verbose_name=_("Warmup Time"))  # WarmupTimeDT
    CookingTime = models.DurationField(default=dt.timedelta(0), verbose_name=_("Cooking Time"))  # CookingTimeDT
    RestTime = models.DurationField(default=dt.timedelta(0), verbose_name=_("Resting Time"))  # RestTimeDT
    TotalTime = models.DurationField(default=dt.timedelta(0), verbose_name=_("Total Time"))   # TotalTimeDT

    GivenWeightKg = models.FloatField(default=0.0, verbose_name=_("Given Weight kg"))  # GivenWeightKg
    InputWeight = models.CharField(default="", max_length=50, verbose_name=_("Input Weight"))  # Weight as given by the user
    OvenTempStandardC = models.IntegerField(default=0, verbose_name=_("Oven Temperature"))  # OvenTempStandardC
    InternalTempStandardC = models.IntegerField(default=0, verbose_name=_("Internal Temperature"))  # InternalTempStandardC
    CountAdults = models.IntegerField(default=0, verbose_name=_("Number of Adults"))  # CountAdults
    CountChildren = models.IntegerField(default=0, verbose_name=_("Number of Children"))  # CountChildren
    CalcType = models.CharField(max_length=20, default="", verbose_name=_("CalcType"))  # CalcType, byWeight or byPerson

    RatingStars = models.IntegerField(blank=True, null=True, default=0,
                                      verbose_name=_("How would you rate our instructions?"), choices=Ratings)
    RatingComment = models.TextField(max_length=1000, blank=True, verbose_name="Tell us how it went...")
    RatingResult = models.IntegerField(choices=CookingOutcomes, blank=True, null=True, default=0,
                                       verbose_name=_("How well was it cooked compared to what you had in mind?"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.User) + ' ' + str(self.PlanName) + ' ' + str(self.updated_at)

    def friendlyname(self):
        return str(self.id) + ' ' + str(self.PlanName) + ' created on ' + str(self.created_at)

    def get_absolute_url(self):
        # A better way TryDjango Video https://www.youtube.com/watch?v=JqbBGxDLQeU
        return reverse('MealPlanDetail', kwargs={'pk': self.id})
