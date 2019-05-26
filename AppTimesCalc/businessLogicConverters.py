def kgToLb():
    return 0.453592

def ovenWarmupTime():
    #how many minutes should you let your oven warm up
    return 15

def niceTime(totalmins):
    if totalmins < 60:
        return str(totalmins) + ' mins'
    else:
        return str(totalmins // 60) + ' h ' + str(totalmins % 60) + ' mins'

def allToKg(w_kg, w_g, w_lb):
    """
    Used to convert three input weights to a KG standard, includes original and unit of original
    """

    w_kg = float(w_kg or 0)
    w_lb = float(w_lb or 0)
    w_g = float(w_g or 0)

    if w_kg:
        return w_kg, w_kg, 'kg'
    elif w_g:
        return w_g / 1000, int(w_g), 'g'
    elif w_lb:
        return w_lb * kgToLb(), w_lb, 'lb'
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