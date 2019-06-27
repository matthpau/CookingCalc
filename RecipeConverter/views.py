from django.shortcuts import render, get_object_or_404
from .forms import RecipeConverter, ConversionUpdateForm
from django.contrib.auth.decorators import login_required
from .businessLogic import converter
from django.views.generic import ListView, UpdateView
from .models import Conversion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


@login_required()
def recipe_converter(request):

    if request.method == 'POST':
        form = RecipeConverter(request.POST)
        if form.is_valid():

            inputs = form.cleaned_data
            inputs['user'] = request.user
            saved_key, outputs = converter(inputs)

            context = {'inputs': inputs, 'saved_key': saved_key, 'outputs': outputs}
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

def converter_about(request):
    return render(request, 'RecipeConverter/converter_about.html')


class ConversionUpdate(UpdateView):
    form_class = ConversionUpdateForm
    template_name = 'RecipeConverter/recipe_update.html'
    success_url = '/converter/saved_conversions'

    def get_object(self):
        id_ = self.kwargs.get('pk')

        result = get_object_or_404(Conversion, id=id_)
        return result

    def form_valid(self, form):
        return super().form_valid(form)


def ConversionDelete(request, pk):

    if request.method == 'POST':

        # https://docs.djangoproject.com/en/2.1/ref/models/querysets/#exists
        entry = Conversion.objects.get(id=pk)
        if Conversion.objects.filter(id=entry.id).exists():

        #  Check we are the logged in user for security
            if request.user == entry.user:
                entry.delete()

        return HttpResponseRedirect('/converter/saved_conversions')

    else:   #get, just showing the record
        ConversionRec = Conversion.objects.get(id=pk)
        context = {"Conversion": ConversionRec}
        return render(request, 'RecipeConverter/conversion_confirm_delete.html', context)
