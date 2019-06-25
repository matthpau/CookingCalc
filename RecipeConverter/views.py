from django.shortcuts import render
from .forms import RecipeConverter
from django.contrib.auth.decorators import login_required
from .businessLogic import converter
from django.views.generic import ListView
from .models import Conversion
from django.contrib.auth.mixins import LoginRequiredMixin


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


class ConversionsList(LoginRequiredMixin, ListView):
    """
    requires login, use LoginRequiredMixin to do this
    https://docs.djangoproject.com/en/2.2/topics/auth/default/#the-loginrequired-mixin
    Context name information https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#making-friendly-template-contexts
    template name can be used but in this case is automatically derived conversion_list from model and view

    context variable name is object_list OR conversion_list, both work. Or you can set your own
     model = MealPlan use this to show ALL meal plans
    """
    def get_queryset(self):
        #  this is how you return only records for the current user
        #  https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/#dynamic-filtering
        return Conversion.objects.filter(user=self.request.user).order_by('-created_at')