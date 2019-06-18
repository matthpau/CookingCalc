# this is run to provide some initial values for which the database works

from django.core.management.base import BaseCommand, CommandError
from AppTimesCalc.models import MeatType, CookingLevel, CookingInfo
from RecipeConverter.models import Converter

# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/


class Command(BaseCommand):

    def handle(self, *args, **options):
        m1 = MeatType(MeatTypeName = "Beef",
                      PortionKGPerAdult=0.4,
                      PortionKGPerChild=0.2,
                      )
        m1.save()

        m2 = MeatType(MeatTypeName="Pork",
                      PortionKGPerAdult=0.4,
                      PortionKGPerChild=0.2,
                      )
        m2.save()

        l1 = CookingLevel(CookingLevel="Rare",
                          CookingLevelSort=10,
                          )
        l1.save()

        l1 = CookingLevel(CookingLevel="Well done",
                          CookingLevelSort=20,
                          )
        l1.save()

        c1 = CookingInfo(MeatType = MeatType.objects.filter(MeatTypeName = "Beef")[0],
                         CookingLevel=CookingLevel.objects.filter(CookingLevel="Rare")[0],
                         OvenTempC=180,
                         InternalTempC=55,
                         MinsPerKg=25,
                         RestTimeMins=10,
                         )
        c1.save()

        c1 = CookingInfo(MeatType=MeatType.objects.filter(MeatTypeName="Beef")[0],
                         CookingLevel=CookingLevel.objects.filter(CookingLevel="Well done")[0],
                         OvenTempC=200,
                         InternalTempC=80,
                         MinsPerKg=40,
                         RestTimeMins=10,
                         )
        c1.save()

        c1 = CookingInfo(MeatType = MeatType.objects.filter(MeatTypeName = "Pork")[0],
                         CookingLevel = CookingLevel.objects.filter(CookingLevel="Rare")[0],
                         OvenTempC = 180,
                         InternalTempC = 55,
                         MinsPerKg = 25,
                         RestTimeMins = 10,
                         )
        c1.save()

        c1 = CookingInfo(MeatType=MeatType.objects.filter(MeatTypeName="Pork")[0],
                         CookingLevel=CookingLevel.objects.filter(CookingLevel="Well done")[0],
                         OvenTempC=200,
                         InternalTempC=80,
                         MinsPerKg=40,
                         RestTimeMins=10,
                         )
        c1.save()

        cv = Converter(unit_source_name='pound',
                       unit_source_keys="'lb', 'pounds', 'pound'",
                       unit_dest_name='kg',
                       unit_conversion=0.453592
                       )
        cv.save()

        cv1 = Converter(unit_source_name='ounce',
                        unit_source_keys="'ounces', 'oz'",
                        unit_dest_name='kg',
                        unit_conversion=0.0283495
                        )
        cv1.save()


