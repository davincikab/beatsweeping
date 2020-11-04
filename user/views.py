from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.conf import settings
from django.core import serializers

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils import timezone

from .token_generator import account_activation_token
from .send_mail import send_activation_mail

from .models import CouponCode, CustomUser, UserProfile
from .forms import SignUpForm, UserProfileForm, PasswordResetForm, ContactForm


import datetime
import json

# Create your views here.
@login_required
def update_profile(request):
    if request.POST:
        user = request.user
        streets_data = process_data(request.POST)
        message = create_update_profile(streets_data, user.email)

        if message != "Success":
            return message
        return JsonResponse({'message':'success', 'navigate_to':'/user_profile/'})

    else:
        user = request.user
        user_profile = UserProfile.objects.filter(user_id = user.pk)
        sections = [f'{entry.section_name}_{entry.oid}' for entry in user_profile]
        phone_number = user_profile[0].phone_number

        # phone_number = phone_number[1:4]+'-'+phone_number[4:7]+'-'+phone_number[7:]
        data = {
            'phone_number':phone_number,
            'email':user_profile[0].email,
            'twelve_hours':user_profile[0].twelve_hours,
            'one_hour':user_profile[0].one_hour,
            'email_notification':user_profile[0].email_notification
        }

        form = UserProfileForm(data)
    return render(request, "index.html", {'form':form, 'sections':sections, 'title':'Update Streets'})

class Login(LoginView):
    template_name = 'user/account/login.html'

class Logout(LogoutView):
    template_name = 'user/account/logout.html'

def register(request):
    if request.user:
        print(request.user)
        return redirect('/update_profile/')
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
            current_site = get_current_site(request)
            message = render_to_string('activate_account.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token':account_activation_token.make_token(user)
            })

            # send mail
            mail_response = send_activation_mail(email, message, 'Account Activation')
            print(mail_response)

            # mail response
            if mail_response != "Success":
                return mail_response

            return JsonResponse({'message':'success', 'navigate_to':f'/activation_email/'})
        else:
            return JsonResponse({'message':'error', 'errors':form.errors})
    else:
        form = SignUpForm()
        user_profile_form = UserProfileForm()

        return render(request, "index.html", {'form':form, 'form_details':user_profile_form, 'title':'Register'})

def email_sent(request):
    return render(request,'email_sent.html')

def faq_view(request):
    return render(request, "faq_views.html")

def contacts_page(request):
    user = None
    if request.user.is_authenticated:
        user = request.user

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # send the mail
            message = f'{form.cleaned_data["email"]}, {form.cleaned_data["message"]}'

            response = send_activation_mail(
                settings.EMAIL_HOST_USER,
                message,
                form.cleaned_data['subject'],
            )
             
            print(response)
            return HttpResponse("Email successfully sent. Thank you.")
    else:
        form = ContactForm()
        if user:
            context = {'form':form, 'uuid':user.pk}
        else:
            context = {'form':form}
        
    return render(request, 'contacts.html', context)

# Process Street section data
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
        [ profile.delete()  for profile in UserProfile.objects.filter(email=email) ]
        for entry in entries:
            user_profile_form = UserProfileForm(entry)
            info = user_profile_form.save(commit=False)
            # info.user = user
            info.oid = entry.get('oid')
            info.section_name = entry.get('section_name')
            info.name = entry.get('name', 'None')
            info.email = email
            info.date_registered = datetime.datetime.now()
            info.user_id = user.id

            print("Saved")
            info.save()
        return "Success"
    else:
        print(form.errors)
        return JsonResponse({"message":"error", 'errors':form.errors })

# Activate user Account
def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(uid)
        user = CustomUser.objects.get(pk = uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, message='Your account has been activated successfully')

        # login the user and redirect to payment page
        login(request, user)
        return redirect(f'/process_payment/')

        # return HttpResponse('Your account has been activated successfully')
    else:
        return HttpResponse("Invalid activation link")
 

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect(reverse('password_reset_done'))
    else:
        form = PasswordResetForm()
    return render(request, 'user/registration/password_reset_form.html', {'form':form})


# User profile section
@login_required 
def user_section(request):
    user = request.user

    user_profile = UserProfile.objects.filter(email=user.email)
    print(user_profile)
    # Create  a dictionary with user info
    user_info = {'sections':[], 'uuid':user.pk}
    i = 1
    for entry in user_profile:
        print(entry)
        user_info['sections'].append(entry.section_name)
        i += 1
    
    # add other information
    if len(user_info['sections']) > 0:
        user_info = {**user_info, 'info':user_profile[0], 'is_subscribed':user.is_subscribed}
    else:
        user_info = {'uuid':user.pk, 'is_subscribed':user.is_subscribed}

    print(user_info)
    return render(request, 'user/account/user_info.html', {'user_info':user_info, 'notify':user.disabled_notification})

# Disable user notification
def disable_notifications(request):
    user = request.user
    if request.method == 'POST':
        # update the userpreform
        notification_state = request.POST.get('notify')
        user = CustomUser.objects.get(email=user.email)
        user.disabled_notification = notification_state
        user.email_notification = notification_state
        user.save()

        # update profile form
        user_profiles = UserProfile.objects.filter(email = user.email)
        for user_profile in user_profiles:
            user_profile.disabled = notification_state
            user_profile.email_notification = notification_state
            user_profile.save()

    return HttpResponse(json.dumps({'message':'success', 'navigate_to':f'/user_profile/'}))


# PAYMENT
@login_required
def process_subscription(request):
    if request.method == "POST":
        # process the data and update the database
        print(request.POST)
        subscription_date = timezone.now()

        user = request.user
        user.is_subscribed = 'Y'
        user.subscription_date = subscription_date.date()
        user.subscription_id = request.POST.get('subscription_id')

        user.save()
        
        return HttpResponse(json.dumps({'message':'success'}))

    else:
        return render(request, 'user/payment/process_subscription.html')

@csrf_exempt
def payment_done(request):
    return render(request, 'user/payment/payment_done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'user/payment/payment_cancelled.html')


# Working with promo code
def process_promo_code(request):
    code = request.POST['promo_code']
    
    try:
         promo_code = CouponCode.objects.get(code=code)
    except CouponCode.DoesNotExist:
        print('Inexistent Promo code')
        return HttpResponse('Inexistent Promo code')

    if promo_code.isUsed:
        return HttpResponse('Promo Code has been used or expired')
    else:
        promo_code.isUsed = True
        promo_code.save()

        user = request.user
        user.is_subscribed = 'Y'
        user.subscription_date = timezone.now()
        user.subscription_id = code

        user.save()

        return HttpResponse('Success')
