from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import authenticate, get_user_model
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .send_mail import send_activation_mail
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
        widget = forms.TextInput(attrs={'placeholder':'myusername', 'autofocus': ''})
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
                attrs={'placeholder':'9347897879', 'pattern':"[0-9]{10}"}
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

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email", max_length=254,
        help_text="Email such a example@gmail.com",
        widget=forms.EmailInput(
            attrs={'placeholder':'example@gmail.com', })
    )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()


    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.

        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            # self.send_mail(subject_template_name, email_template_name,
            #                context, from_email, user.email,
            #                html_email_template_name=html_email_template_name)
            
            message = render_to_string(email_template_name, {
                'email':user.email,
                'domain':domain,
                'site_name':site_name,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'user':user,
                'token':token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            })

            send_activation_mail(user.email, message, "BeatSweeping Password Reset")
        

# Contact form
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        fields = ['email', 'message']