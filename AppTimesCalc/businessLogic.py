from .models import CookingInfo
from .businessLogicConverters import *
import datetime as dt

def CookCalc(inputVals):
    """
    Expects context dictionary from the CookingCalc.html form document
    Weightin Kilos and keys for meat type and cooking level
    Returns dictionary with weight, meat type, cooking level, recommended cooking time and oven temps
    Input Vars Weight_kg / Weight_lb / Weight_g / EatingTime / MeatType Key / CookingLevel Key
    """
    results = dict()
    print(inputVals)

    c = CookingInfo.objects.filter(MeatType = inputVals['MeatType']).\
            filter(CookingLevel = inputVals['CookingLevel'])

    if c.exists():
        c = c.values()[0]

        weightResult = allToKg(inputVals['Weight_kg'], inputVals['Weight_g'], inputVals['Weight_lb'])
        givenWeightKg = weightResult[0]

        cookingMins = int(c['MinsPerKg'] * givenWeightKg + c['MinsFixed'])
        totalMins = cookingMins + c['RestTimeMins'] + ovenWarmupTime()


        if inputVals['EatingTime']:
            DTeatingtime = dt.datetime.combine(dt.date.today(), inputVals['EatingTime'])
            DTcookingMins = dt.timedelta(minutes=cookingMins)
            DTtotalMins = dt.timedelta(minutes=totalMins)
            DTwarmupMins = dt.timedelta(minutes=ovenWarmupTime())
            DTrestMins = dt.timedelta(minutes=c['RestTimeMins'])

            results['StartTime'] = (DTeatingtime - DTrestMins - DTcookingMins -  DTwarmupMins)
            results['MeatInTime'] = (results['StartTime'] + DTwarmupMins)
            results['RemoveTime'] = (results['MeatInTime'] + DTcookingMins).time()
            results['EatingTime'] = inputVals['EatingTime']

            results['StartTime'] = results['StartTime'].time()
            results['MeatInTime'] =results['MeatInTime'].time()

        results['Valid'] = True
        results['NotRecommended'] = c['NotRecommended']
        results['WarmupTime'] = niceTime(ovenWarmupTime())
        results['CookingTime'] = niceTime(cookingMins)
        results['RestTime'] = niceTime(c['RestTimeMins'])
        results['TotalTime'] = niceTime(totalMins)
        results['InputWeight'] = str(weightResult[1]) + ' ' + str(weightResult[2])
        results['WeightStandardkg'] = str(round(givenWeightKg, 1)) + ' kg'
        results['OvenTemp'] = str(c['OvenTempC']) + '° C or ' + str(CtoF(c['OvenTempC'])) + '° F'
        results['InternalTemp'] = str(c['InternalTempC']) + '° C or ' + str(CtoF(c['InternalTempC'])) + '° F'

    else:
        results['Notice:'] = 'uppsala'

    return results
