from django.shortcuts import render
from .forms import UserForm, ProfileForm
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages

def update_profile(request):
    from .models import Profile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated'))

            # Transfer the temp objecs to the perm ones and then delete
            u = Profile.objects.get(user=request.user)
            print(u, u.id)
            print('TEMP', u.temp_location)
            print('TEMP', u.temp2)

            if u.temp_location and u.temp2:
                print('Found new details, updating and clearing')
                a = u.temp_location
                b = u.temp2

                u.found_location = a
                u.found_address = b
                u.temp_location = ''
                u.temp2 = ''
                print('FOUND', u.found_location)
                print('FOUND',u.found_address)
                print('TEMP', u.temp_location)
                print('TEMP', u.temp2)

                u.save()

                print('post save------')

                print('FOUND', u.found_location)
                print('FOUND',u.found_address)
                print('TEMP', u.temp_location)
                print('TEMP', u.temp2)

                #Reinstantiate to refresh the forms


        else:
            messages.error(request, ('Please correct the error.'))
    else: # GET
        print('doing a get')
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html',{
        'user_form': user_form,
        'profile_form': profile_form
    })

def check_address(request):
    from django.contrib.gis.geos import fromstr
    from geopy.geocoders import Nominatim
    from .businessLogic import nice_address
    from .models import Profile, CustomUser
    #email = request.POST.get('email')

    input_addr = (
        request.POST.get('add_1'),
        request.POST.get('add_2'),
        request.POST.get('city'),
        request.POST.get('postcode'),
        request.POST.get('country'),
    )

    input_addr = nice_address(*input_addr)

    geolocator = Nominatim(user_agent="CookingCalc")
    found_addr = geolocator.geocode(input_addr)
    
    p = Profile.objects.get(user=request.user)
    if found_addr:
            
        lat, lon = (found_addr.latitude, found_addr.longitude)
        found_loc = fromstr(f'POINT({lon} {lat})', srid=4326)


        #print('XXXX', u.temp_address)
        p.temp_location = found_loc
        p.temp_address = found_addr.address
        p.temp2 = found_addr.address
        p.save()
        #p.save(update_fields=['temp_location', 'temp_address'])

        print('YYYY', p.temp_location)
        print('YYYY', p.temp2)

        data = {"found_address": found_addr.address}

    else: # could not geolocate
        print('geolocation failed')
        p.temp_location = ''
        p.temp_address = ''
        data = {"found_address": 'Could not find this address'}

    return JsonResponse(data)
