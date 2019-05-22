

from .models import CookingInfo

def CookCalc(context):
    #Expects context dictionary from the CookingCalc.html form document
    #Weightin Kilos and keys for meat type and cooking level
    #Returns dictionary with weight, meat type, cooking level, recommended cooking time and oven temps
    #Input Vars Weight / MeatType Key / Cooking Level Key

    c = Cookinfo.objects.all()

    for a, b in enumerate(context):
        print(a,b)

    print(c)

    pass

