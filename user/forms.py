from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

# from .send_mail import send_activation_mail
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, CustomUser

SMS_TIME = (
        ('Y', 'Yes'),
        ('N', 'No')
    )

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, 
            help_text="Email such a example@gmail.com",
            widget=forms.EmailInput(
                attrs={'placeholder':'example@gmail.com', }
            )
        )
    username = forms.CharField(label="Username", max_length=50, required=True,
        help_text = "Enter you username",
        widget = forms.TextInput(attrs={'placeholder':'myusername',})
    )

    password1 = forms.CharField(label="Password", max_length=50, required=True, 
        help_text="",
        widget = forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label="Phone Number", max_length=13, required=True,
            help_text="Phone number format 9347897879",
            widget=forms.TextInput(
                attrs={'placeholder':'9347897879', }
            )
        )
         
    twelve_hours = forms.ChoiceField(
        label="Twelve hours", choices=SMS_TIME, 
        help_text="Recieve notification on every day."
        )

    one_hour = forms.ChoiceField(
        label="One hour", choices=SMS_TIME,
        help_text="Recieve notification on every hour."
        )

    email_notification = forms.ChoiceField(
        label="Email Notification", choices=SMS_TIME,
        help_text="Recieve notification via mail."
        
        )
    class Meta:
        model = UserProfile
        exclude = ['is_subscribed', 'subscription_date', 'subscription_duration',
                     'oid', 'section_name', 'name', 'date_registered', 'user_id','disabled', 'email']
