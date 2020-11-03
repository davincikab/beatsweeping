from django.urls import path
from .views import home, register, faq_view, contacts_page

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path('contacts/', contacts_page, name='contacts'),
    path('faqs/', faq_view, name='faq-view'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
