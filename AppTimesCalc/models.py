from django.db import models
from django.contrib.auth import get_user_model
import datetime as dt
from django.urls import reverse

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
    CookingLevel = models.CharField(max_length = 30, unique=True)
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
            models.UniqueConstraint(fields= ['MeatType','CookingLevel'], name='UniquePerMeat'),
        ]
# https://wsvincent.com/django-referencing-the-user-model/


CookingOutcomes = [('CO1', 'Very undercooked'),
                   ('CO2', 'Undercooked'),
                   ('CO3', 'Just Right'),
                   ('CO4', 'Overcooked'),
                   ('CO5', 'Very Overcooked')]


class MealPlan(models.Model):

    User = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    PlanName = models.CharField(max_length=100)
    PlanDesc = models.TextField(blank=True)
    MeatType = models.ForeignKey(MeatType, on_delete=models.CASCADE) # MeatType
    CookingLevel = models.ForeignKey(CookingLevel, on_delete=models.CASCADE) # CookingLevel

    StartTime = models.TimeField(default=dt.time(0, 0))  # StartTime
    MeatInTime = models.TimeField(default=dt.time(0, 0))  # MeatInTime
    RemoveTime = models.TimeField(default=dt.time(0, 0))   # RemoveTime
    EatingTime = models.TimeField(default=dt.time(0, 0))  # EatingTime

    WarmupTime = models.DurationField(default=dt.timedelta(0))  # WarmupTimeDT
    CookingTime = models.DurationField(default=dt.timedelta(0))  # CookingTimeDT
    RestTime = models.DurationField(default=dt.timedelta(0))  # RestTimeDT
    TotalTime = models.DurationField(default=dt.timedelta(0))   # TotalTimeDT

    GivenWeightKg = models.FloatField(default=0.0)  # GivenWeightKg
    OvenTempStandardC = models.IntegerField(default=0)  # OvenTempStandardC
    InternalTempStandardC = models.IntegerField(default=0)  # InternalTempStandardC
    CountAdults = models.IntegerField(default=0)  # CountAdults
    CountChildren = models.IntegerField(default=0)  # CountChildren
    CalcType = models.CharField(max_length=20, default="")  # CalcType, byWeight or byPerson

    RatingStars = models.IntegerField(blank=True, null=True)
    RatingComment = models.TextField(max_length=1000, blank=True)
    RatingResult = models.CharField(choices=CookingOutcomes, max_length=3, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ' ' + str(self.User) + ' ' + str(self.PlanName) + ' ' + str(self.updated_at)

    def get_absolute_url(self):
        # A better way TryDjango Video https://www.youtube.com/watch?v=JqbBGxDLQeU
        return reverse('MealPlanDetail', kwargs={'pk': self.id})
