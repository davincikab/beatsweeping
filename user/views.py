from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import CouponCode, CustomUser, UserProfile
from .forms import SignUpForm, UserProfileForm


import datetime
import json

# Create your views here.
def home(request):
    form = SignUpForm()
    return render(request, "index.html", {'form':form})

def register(request):
    if request.POST:
        form = SignUpForm(request.POST)

        # validate form
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False

            user.save()
            print(form.cleaned_data)

            # update profile table
            email = form.cleaned_data['email']
            streets_data = process_data(request.POST)
            message = create_update_profile(streets_data, email)

            if message == "error":
                # delete the user with the given email
                user = CustomUser.objects.get(email = email)
                user.delete()

                # delete the related fields
                [ profile.delete()  for profile in UserProfile.objects.filter(email=email) ]

                return JsonResponse({'message':'error', 'errors':form.errors})

            # send mail
            return JsonResponse({'message':'success', 'navigate_to':f'/activation_email/'})
        else:
            return JsonResponse({'message':'error', 'errors':form.errors})
    else:
        form = SignUpForm()
        user_profile_form = UserProfileForm()

        return render(request, "index.html", {'form':form, 'form_details':user_profile_form})

def email_sent(request):
    return render(request,'email_sent.html')

def faq_view(request):
    return render(request, "faq_views.html")

def contacts_page(request):
    return render(request, "contacts.html")

def process_data(data):
    streets = []

    for k, v in data.items():
        if k.startswith('res'):
            street = v.split('_')

            data_dict = {
                'oid':int(street[1]),
                'section_name':street[0],
                'name':data.get('name'),
                'phone_number': data.get("phone_number"),
                'email':data.get('email'),
                'twelve_hours':data.get('twelve_hours', 'N'),
                'one_hour':data.get('one_hour', 'N'),
                'email_notification':data.get('email_notification', 'N')
            }

            streets.append(data_dict)
    
    print(streets)
    return streets

def create_update_profile(entries, email):
    form = UserProfileForm(entries[0])
    user = CustomUser.objects.get(email=email)

    # process data
    if form.is_valid():
        for entry in entries:
            user_profile_form = UserProfileForm(entry)
            info = user_profile_form.save(commit=False)
            # info.user = user
            info.oid = entry.get('oid')
            info.section_name = entry.get('section_name')
            info.name = entry.get('name', 'None')
            info.email = entry.get('email')
            info.date_registered = datetime.datetime.now()
            info.user_id = user.id

            print("Saved")
            info.save()
        return HttpResponse("Success")
    else:
        print(form.errors)
        return HttpResponse("Error")