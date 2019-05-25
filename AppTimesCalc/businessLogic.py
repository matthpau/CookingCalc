from .models import CookingInfo
from .businessLogicConverters import *

def CookCalc(inputVals):
    """
    Expects context dictionary from the CookingCalc.html form document
    Weightin Kilos and keys for meat type and cooking level
    Returns dictionary with weight, meat type, cooking level, recommended cooking time and oven temps
    Input Vars Weight / MeatType Key / Cooking Level Key
    """
    results = dict()

    c = CookingInfo.objects.filter(MeatType = inputVals['MeatType']).\
            filter(CookingLevel = inputVals['CookingLevel'])
    #TODO this section is not finished

    #https://docs.djangoproject.com/en/2.2/ref/models/querysets/#exists

    c = CookingInfo.objects.filter(MeatType=inputVals['MeatType']). \
        filter(CookingLevel=inputVals['CookingLevel'])

    if c.exists():
        c = c.values()[0]
        print(inputVals)
        print(c)

        weightResult = allToKg(inputVals['Weight_kg'], inputVals['Weight_g'], inputVals['Weight_lb'])
        givenWeightKg = weightResult[0]

        cookingMins = int(c['MinsPerKg'] * givenWeightKg + c['MinsFixed'])
        cookingHrs = str(cookingMins // 60) + ' h ' + str(cookingMins % 60) + ' mins'

        results['InputWeight'] = allToKgRev(weightResult)
        results['WeightStandardkg'] = str(round(givenWeightKg, 1)) + ' kg'
        results['CookingTime'] =  str(cookingMins) + ' mins or ' + cookingHrs
        results['OvenTemp'] = str(c['OvenTempC']) + '° C or ' + str(CtoF(c['OvenTempC'])) + '° F'
        results['InternalTemp'] = str(c['InternalTempC']) + '° C or ' + str(CtoF(c['InternalTempC'])) + '° F'

    else:
        results['Notice:'] = 'uppsala'

    return results
