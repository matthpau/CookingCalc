from django.db import models
from django.contrib.auth import get_user_model

#https://docs.djangoproject.com/en/2.2/ref/models/options/
#https://docs.djangoproject.com/en/2.2/ref/models/fields/
#https://docs.djangoproject.com/en/2.2/ref/models/constraints/
#https://docs.djangoproject.com/en/2.2/ref/models/relations/
#https://docs.djangoproject.com/en/2.2/topics/db/queries/#lookups-that-span-relationships


class MeatType(models.Model):
    MeatTypeName = models.CharField(max_length=60)
    PortionKGPerAdult = models.FloatField(default=0)
    PortionKGPerChild = models.FloatField(default=0)

    def __str__(self):
        return self.MeatTypeName

    class Meta:
        ordering = ['MeatTypeName']

class CookingLevel(models.Model):
    CookingLevel = models.CharField(max_length = 30)
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
    RestTimeMins =models.IntegerField(default=0)

    def __str__(self):
        return str(self.MeatType) + ' ' + str(self.CookingLevel)

    class Meta:
        verbose_name_plural = 'CookingInfo'
        ordering = ['MeatType', 'CookingLevel__CookingLevelSort']
        constraints = [
            models.UniqueConstraint(fields= ['MeatType','CookingLevel'], name='UniquePerMeat'),
        ]


class MealPlan(models.Model):
    UserId = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    PlanName = models.CharField(max_length=100)
    MeatType = models.ForeignKey(MeatType, on_delete=models.CASCADE) #MeatType
    CookingLevel = models.ForeignKey(CookingLevel, on_delete=models.CASCADE) #CookingLevel

    StartTime = models.TimeField(default="00:00")  # StartTime
    MeatInTime = models.TimeField(default="00:00")  # MeatInTime
    RemoveTime = models.TimeField(default="00:00")   # RemoveTime
    EatingTime = models.TimeField(default="00:00") # EatingTime
    WarmupTime = models.DurationField(default=0)  # WarmupTimeDT
    CookingTime = models.DurationField(default=0)  # CookingTimeDT
    RestTime = models.DurationField(default=0)  # RestTimeDT
    TotalTime = models.DurationField(default=0)   # TotalTimeDT
    GivenWeightKG = models.FloatField(default=0.0) # GivenWeightKg
    OvenTempStandardC = models.IntegerField(default=0)  # OvenTempStandardC
    InternalTempStandardC = models.IntegerField(default=0)  # InternalTempStandardC
    CountAdults = models.IntegerField(default=0)  # CountAdults
    CountChildren = models.IntegerField(default=0)  # CountChildren
    CalcType = models.CharField(max_length=20, default = "")  # CalcType, byWeight or byPerson

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.UserId) + ' ' + str(self.PlanName)
"""
Output from a calculation
0 MeatType Beef <class 'AppTimesCalc.models.MeatType'>
1 CookingLevel Rare <class 'AppTimesCalc.models.CookingLevel'>
2 StartTime 12:17:00 <class 'datetime.time'>
3 MeatInTime 12:32:00 <class 'datetime.time'>
4 RemoveTime 13:50:00 <class 'datetime.time'>
5 EatingTime 14:00:00 <class 'datetime.time'>
6 Valid True <class 'bool'>
7 NotRecommended False <class 'bool'>
8 WarmupTime 15 mins <class 'str'>
9 WarmupTimeDT 0:15:00 <class 'datetime.timedelta'>
10 CookingTime 1 h 18 mins <class 'str'>
11 CookingTimeDT 1:18:00 <class 'datetime.timedelta'>
12 RestTime 10 mins <class 'str'>
13 RestTimeDT 0:10:00 <class 'datetime.timedelta'>
14 TotalTime 1 h 43 mins <class 'str'>
15 TotalTimeDT 1:43:00 <class 'datetime.timedelta'>
16 InputWeight 3.14  kg <class 'str'>
17 GivenWeightKg 3.14 <class 'float'>
18 WeightStandardkg 3.1 kg <class 'str'>
19 WeightStandardlb 6.9 lb <class 'str'>
20 OvenTempStandardC 180 <class 'int'>
21 OvenTemp 180° C or 356° F <class 'str'>
22 InternalTempStandardC 55 <class 'int'>
23 InternalTemp 55° C or 131° F <class 'str'>
24 CountAdults None <class 'NoneType'>
25 CountChildren None <class 'NoneType'>
26 Portion_gPerAdult 400 g <class 'str'>
27 calcAdults 7 <class 'int'>
28 Portion_gPerChild 200 g <class 'str'>
29 CalcType byWeight <class 'str'>

"""
