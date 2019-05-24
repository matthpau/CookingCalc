from .models import CookingInfo

def allToKg(w_kg, w_gr, w_lb):

    w_kg = float(w_kg)
    w_lb = float(w_lb)
    w_gr = float(w_gr)

    if w_kg:
        return w_kg, 1
    elif w_g:
        return w_g / 1000, 2
    elif w_lb:
        return w_lb * 0.453592, 3
    else:
        return 0, 0


def CookCalc(context):
    """
    Expects context dictionary from the CookingCalc.html form document
    Weightin Kilos and keys for meat type and cooking level
    Returns dictionary with weight, meat type, cooking level, recommended cooking time and oven temps
    Input Vars Weight / MeatType Key / Cooking Level Key
    """
    results = dict()

    try:
        c = CookingInfo.objects.filter(MeatType = context['MeatType']).\
            filter(CookingLevel = context['CookingLevel']).values()[0]

        weightResult = allToKg(context['Weight_kg'], context['Weight_g'], context['Weight_lb'])
        givenWeight = weightResult[0]

        minsPerKg = c['MinsPerKg']
        results['Cooking Time'] =  int(minsPerKg * givenWeight)
        results['Oven Temperature'] = c['OvenTempC']
        results['Final Internal Temperature'] = c['InternalTempC']
        print(c)
    except:
        results['Notice:'] = 'Invalid combination'

    return results

