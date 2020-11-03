from django.shortcuts import render

from .models import CouponCode, CustomUser, UserProfile
from .forms import SignUpForm, UserProfileForm

# Create your views here.
def home(request):
    form = SignUpForm()
    return render(request, "index.html", {'form':form})

def register(request):
    form = SignUpForm()
    user_profile = UserProfileForm()
    return render(request, "index.html", {'form':form, 'form_details':user_profile})

def faq_view(request):
    return render(request, "faq_views.html")

def contacts_page(request):
    return render(request, "contacts.html")
