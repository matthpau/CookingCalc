from .models import CookingInfo

def CookCalc(context):
    #Expects context dictionary from the CookingCalc.html form document
    #Weightin Kilos and keys for meat type and cooking level
    #Returns dictionary with weight, meat type, cooking level, recommended cooking time and oven temps
    #Input Vars Weight / MeatType Key / Cooking Level Key

    givenweight = float(context['Weight'])

    results = dict()

    try:
        c = CookingInfo.objects.filter(MeatType = int(context['MeatType'][0])).\
            filter(CookingLevel = int(context['CookingLevel'][0])).values()[0]

    except:
        results['Cooking Time'] = 0
    else:
        minsPerKg = int(c['MinsPerKg'])
        results['Cooking Time'] =  int(minsPerKg * givenweight)

    return results

