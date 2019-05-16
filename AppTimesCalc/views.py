from django.shortcuts import render
from django.http import HttpResponse

def Calculator(request):
    return render(request, 'AppTimesCalc/CookingCalc.html')

def UserPage(request):
    return render(request, 'AppTimesCalc/UserPage.html')
