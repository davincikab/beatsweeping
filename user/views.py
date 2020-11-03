from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "base.html")

def register(request):
    return render(request, "user/account/register.html")

def faq_view(request):
    return render(request, "faq_views.html")

def contacts_page(request):
    return render(request, "contacts.html")
