from django.shortcuts import render
from django.http import  HttpResponse
from .forms import RecipeConverter
from django.contrib.auth.decorators import login_required
from .businessLogic import converter

#from django.shortcuts import render, redirect, get_object_or_404
#from .models import *

#from django.views.generic import ListView, UpdateView, DetailView, DeleteView
#from django.contrib.auth.mixins import LoginRequiredMixin
#from django.conf import settings
#from users.models import CustomUser


@login_required()
def recipe_converter(request):

    if request.method == 'POST':
        form = RecipeConverter(request.POST)
        if form.is_valid():

            inputs = form.cleaned_data
            inputs['user'] = request.user
            conversions, outputs = converter(inputs)

            context = {'inputs': inputs,
                       'outputs': outputs,
                       'conversions': conversions}
            return render(request, 'RecipeConverter/converter_results.html', context)

    else:
        form = RecipeConverter()  # initial get for display

    context = {'form': form}

    return render(request, 'RecipeConverter/recipe_converter.html', context)


def saved_conversions(request):
    return render(request, 'RecipeConverter/saved_conversions.html')
