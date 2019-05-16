from django.db import models

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
    InitialOvenTempC = models.IntegerField(default=0)
    OvenTempC = models.IntegerField(default=0)
    InternalTempC = models.IntegerField(default=0)
    InitialOvenTimeMins = models.IntegerField(default=0)
    MinsPerKg = models.IntegerField(default=0)
    MinsFixed = models.IntegerField(default=0)

    def __str__(self):
        return str(self.MeatType) + ' ' + str(self.CookingLevel)

    class Meta:
        verbose_name_plural = 'CookingInfo'
        ordering = ['MeatType', 'CookingLevel__CookingLevelSort']
        constraints = [
            models.UniqueConstraint(fields= ['MeatType','CookingLevel'], name='UniquePerMeat'),
        ]

class CookingPlan(models.Model):
    UserId = models.IntegerField(default=0)
    PlanName = models.CharField(max_length=300, blank=True)
    MeatType = models.ForeignKey(MeatType, on_delete=models.CASCADE)
    CookingLevel = models.ForeignKey(CookingLevel, on_delete=models.CASCADE)
    InitialOvenTempC = models.IntegerField(default=0)
    OvenTempC = models.IntegerField(default=0)
    InternalTempC = models.IntegerField(default=0)
    InitialOvenTimeMins = models.IntegerField(default=0)
    MinsPerKg = models.IntegerField(default=0)
    MinsFixed = models.IntegerField(default=0)
    AdultsCount = models.IntegerField(default=0)
    ChildrenCount = models.IntegerField(default=0)
    MealSizeScaling = models.IntegerField(default=1)
    EatingTime = models.TimeField(blank=True)
    CookingTime = models.TimeField(blank=True)
    CookingStart = models.TimeField(blank=True)
    RecordCreated = models.DateTimeField(auto_now_add=True)
    RecordModified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ID) + ' ' + str(self.PlanName)
