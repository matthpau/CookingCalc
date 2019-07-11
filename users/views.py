from django.shortcuts import render
from .forms import UserForm, ProfileForm
from django.http import HttpResponseRedirect
from django.contrib import messages

def update_profile(request):
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, ('Your profile was successfully updated'))
                return HttpResponseRedirect('/')
            else:
                messages.error(request, ('Please correct the error.'))
        else: # GET
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)

        return render(request, 'users/profile.html',{
            'user_form': user_form,
            'profile_form': profile_form
        })
