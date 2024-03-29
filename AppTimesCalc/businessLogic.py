from .models import *
from .businessLogicConverters import *
import datetime as dt
from users.models import CustomUser

from django.contrib.auth import get_user_model


def CookCalc(inputVals):
    """
    Expects context dictionary from the CookingCalc_w.html form document
    Weightin Kilos and keys for meat type and cooking level
    Returns dictionary with weight, meat type, cooking level, recommended cooking time and oven temps
    Input Vars Weight_kg / Weight_lb / Weight_g / EatingTime / MeatType Key / CookingLevel Key
    CalcType: byWeight/byPerson depends on which form triggered this routine
    """
    results = dict()

    #Get the meat and cooking info
    c = CookingInfo.objects.filter(MeatType=inputVals['MeatType']).filter(CookingLevel=inputVals['CookingLevel'])
    d = MeatType.objects.filter(MeatTypeName=inputVals['MeatType']).values()[0]

    if c.exists():
        c = c.values()[0]

        if inputVals['CalcType'] == 'byWeight':
            #When by Weight, CountAdults and CountChildren are missing from the inputs, need to be added in
            inputVals['CountAdults'] = 0
            inputVals['CountChildren'] = 0

            weightResult = allToKg(inputVals['Weight_kg'], inputVals['Weight_g'], inputVals['Weight_lb'])

        else:

            calcWeight = (inputVals['CountAdults'] or 0) * d['PortionKGPerAdult']
            calcWeight += (inputVals['CountChildren'] or 0) * d['PortionKGPerChild']
            weightResult = allToKg(calcWeight, 0, 0)


        givenWeightKg = weightResult[0]
        calcAdults = int(givenWeightKg // d['PortionKGPerAdult'])

        cookingMins = int(c['MinsPerKg'] * givenWeightKg + c['MinsFixed'])
        totalMins = cookingMins + c['RestTimeMins'] + ovenWarmupTime()

        DTeatingtime = dt.datetime.combine(dt.date.today(), inputVals['EatingTime'])
        DTcookingMins = dt.timedelta(minutes=cookingMins)
        DTtotalMins = dt.timedelta(minutes=totalMins)
        DTwarmupMins = dt.timedelta(minutes=ovenWarmupTime())
        DTrestMins = dt.timedelta(minutes=c['RestTimeMins'])
        DTBrowningMins = dt.timedelta(minutes=c['BrowningMins'])

        results['MeatType'] = inputVals['MeatType']
        results['CookingLevel'] = inputVals['CookingLevel']
        results['StartTime'] = (DTeatingtime - DTrestMins - DTcookingMins -  DTwarmupMins)
        results['MeatInTime'] = (results['StartTime'] + DTwarmupMins)
        results['RemoveTime'] = (results['MeatInTime'] + DTcookingMins).time()
        results['EatingTime'] = inputVals['EatingTime']
        results['StartTime'] = results['StartTime'].time()
        results['MeatInTime'] = results['MeatInTime'].time()
        results['Valid'] = True
        results['NotRecommended'] = c['NotRecommended']
        results['WarmupTime'] = niceTime(ovenWarmupTime())
        results['WarmupTimeDT'] = DTwarmupMins
        results['BrowningMins'] = DTBrowningMins
        results['CookingTime'] = niceTime(cookingMins)
        results['CookingTimeDT'] = DTcookingMins
        results['RestTime'] = niceTime(c['RestTimeMins'])
        results['RestTimeDT'] = DTrestMins
        results['TotalTime'] = niceTime(totalMins)
        results['TotalTimeDT'] = DTtotalMins
        results['InputWeight'] = str(round(weightResult[1], 3)) + str(weightResult[2])
        results['GivenWeightKg'] = round(givenWeightKg, 3)
        results['WeightStandardkg'] = str(round(givenWeightKg, 1)) + ' kg'
        results['WeightStandardlb'] = str(round(givenWeightKg*kgToLb(), 1)) + ' lb'
        results['BrowningTempStandardC']  = c['BrowningTempC']
        results['BrowningTemp'] = OvenTempPretty(c['BrowningTempC'])
        results['OvenTempStandardC'] = c['OvenTempC']
        results['OvenTemp'] = OvenTempPretty(c['OvenTempC'])
        results['InternalTempStandardC'] = c['InternalTempC']
        results['InternalTemp'] = OvenTempPretty(c['InternalTempC'])
        results['CountAdults'] = inputVals['CountAdults'] or 0
        results['CountChildren'] = inputVals['CountChildren'] or 0
        results['Portion_gPerAdult'] = str(round(d['PortionKGPerAdult']*1000)) + ' g'
        results['calcAdults'] = calcAdults
        results['Portion_gPerChild'] = str(round(d['PortionKGPerChild']*1000)) + ' g'
        results['CalcType'] = inputVals['CalcType']

    else:
        results['Notice:'] = 'uppsala'

    return results

def AddMeal(saveData):
    """
    saves the calculation
    :param request:
    :param saveData: the saved data from the input
    :return: the PK of the newly saved record
    """

    getMeatType = MeatType.objects.get(MeatTypeName=saveData['MeatType'])
    getCookingLevel = CookingLevel.objects.get(CookingLevel=saveData['CookingLevel'])

    if saveData['planName']:
        planName = saveData['planName']
    else:
        planName = str(saveData['InputWeight']) + ' ' + str(getMeatType).lower() + ', ' + str(getCookingLevel).lower()

    m = MealPlan(User=saveData['User'],
                 PlanName=planName,
                 PlanDesc='(Add any comments here...)',
                 MeatType=getMeatType,
                 CookingLevel=getCookingLevel,
                 StartTime=saveData['StartTime'],
                 MeatInTime=saveData['MeatInTime'],
                 RemoveTime=saveData['RemoveTime'],
                 EatingTime=saveData['EatingTime'],
                 WarmupTime=saveData['WarmupTimeDT'],
                 CookingTime=saveData['CookingTimeDT'],
                 RestTime=saveData['RestTimeDT'],
                 TotalTime=saveData['TotalTimeDT'],
                 GivenWeightKg=saveData['GivenWeightKg'],
                 InputWeight=saveData['InputWeight'],
                 OvenTempStandardC=saveData['OvenTempStandardC'],  # OvenTempStandardC
                 InternalTempStandardC=saveData['InternalTempStandardC'],  # InternalTempStandardC
                 CountAdults=saveData['CountAdults'],  # CountAdults
                 CountChildren=saveData['CountChildren'],  # CountChildren
                 CalcType=saveData['CalcType'],
                 )
    m.save()
    return m.pk



