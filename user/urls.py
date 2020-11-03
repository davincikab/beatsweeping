from django.urls import path, re_path

from .views import home, register, faq_view, contacts_page, email_sent, activate_account, Login, Logout, password_reset
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path('contacts/', contacts_page, name='contacts'),
    path('faqs/', faq_view, name='faq-view'),

    path("register/", register, name="register"),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout .as_view(), name='logout'),

    # password reset
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', password_reset, name='password_reset'),
    path('accounts/password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name="user/registration/password_reset_done.html"), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="user/registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="user/registration/password_reset_complete.html"), name='password_reset_complete'),


    path("activation_email/", email_sent, name="email-sent"),
    re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate_account, name='activate'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
