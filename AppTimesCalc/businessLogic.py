from .models import CookingInfo

def kgToLb():
    return 0.453592

def allToKg(w_kg, w_g, w_lb):

    w_kg = float(w_kg or 0)
    w_lb = float(w_lb or 0)
    w_g = float(w_g or 0)

    if w_kg:
        return w_kg, w_kg, 'kg'
    elif w_g:
        return w_g / 1000, w_kg, 'g'
    elif w_lb:
        return w_lb * kgToLb(), w_kg, 'lb'
    else:
        return 0, 0, 0

def kgTo(w_kg, toValue):
    if toValue == 1:
        return str(w_kg) + 'kg'
    elif toValue == 2:
        return str(w_kg*1000) + 'g'
    elif toValue == 3:
        return str(w_kg/kgToLb()) + 'lb'

def CtoF(CValue):
    return int((CValue * 9 / 5) + 32)


def CookCalc(context):
    """
    Expects context dictionary from the CookingCalc.html form document
    Weightin Kilos and keys for meat type and cooking level
    Returns dictionary with weight, meat type, cooking level, recommended cooking time and oven temps
    Input Vars Weight / MeatType Key / Cooking Level Key
    """
    results = dict()

    c = CookingInfo.objects.filter(MeatType = context['MeatType']).\
            filter(CookingLevel = context['CookingLevel'])
    #TODO this section is not finished

    #https://docs.djangoproject.com/en/2.2/ref/models/querysets/#exists

    c = CookingInfo.objects.filter(MeatType=context['MeatType']). \
        filter(CookingLevel=context['CookingLevel'])

    if c.exists():
        c = c.values()[0]
        print(c)

        weightResult = allToKg(context['Weight_kg'], context['Weight_g'], context['Weight_lb'])
        givenWeight = weightResult[0]

        if weightResult[2] == 'kg':
            results['Input weight'] = str(context['Weight_kg']) + ' kg'
        elif weightResult[2] == 'g':
            results['Input weight'] = str(context['Weight_g']) + ' g'
        elif weightResult[2] == 'lb':
            results['Input weight'] = str(context['Weight_lb']) + ' lb'

        results['Weight Standard kg'] = str(round(givenWeight, 1)) + ' kg'
        results['Cooking_Time'] =  str(int(c['MinsPerKg'] * givenWeight + c['MinsFixed'])) + ' mins'
        results['Oven Temperature'] = str(c['OvenTempC']) + '° C or ' + str(CtoF(c['OvenTempC'])) + '° F'
        results['Internal Temperature'] = str(c['InternalTempC']) + '° C or ' + str(CtoF(c['InternalTempC'])) + '° F'

    else:
        results['Notice:'] = 'uppsala'

    return results