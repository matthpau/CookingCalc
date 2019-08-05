from django.shortcuts import render
from .forms import UserForm, ProfileForm
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import CustomUser

from django.contrib.auth import logout

@login_required()
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, (_('Your profile was successfully updated')))
            return HttpResponseRedirect ('/')

        #else:
        #    messages.error(request, ('Please correct the error.'))
    
    else: # GET
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html',
    {
        'user_form': user_form,
        'profile_form': profile_form
    })

def check_address(request):
    from geopy.geocoders import Nominatim
    from .businessLogic import nice_address

    input_addr = (
        request.POST.get('house_number'),
        request.POST.get('street'),
        request.POST.get('add_2'),
        request.POST.get('city'),
        request.POST.get('postcode'),
        request.POST.get('country'),
    )

    input_addr = nice_address(*input_addr)
    geolocator = Nominatim(user_agent="CookingCalc")
    #TODO need to add a try except here for the timeout
    found_addr = geolocator.geocode(input_addr, timeout=5)
    
    if found_addr:
        data = {
            "success": True,
            "found_address": found_addr.address
            }

    else: # could not geolocate
        data = {
            "success": False,
            "found_address": 'Could not find this address'
            }

    return JsonResponse(data)

@login_required()
def delete_confirm(request):
    return render(request, 'users/delete_confirm.html')

@login_required()
def delete(request):
    user_id = request.user.id
    logout(request)
    CustomUser.objects.get(id=user_id).delete()
    return HttpResponseRedirect('/')
