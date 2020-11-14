from django.urls import path, re_path

from .views import update_profile, register, faq_view, contacts_page, email_sent, activate_account, \
    Login, Logout, password_reset, user_section, disable_notifications, process_promo_code, \
    process_subscription, payment_canceled, payment_done, get_alert

from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("update_profile/", update_profile, name="update-profile"),
    path('contacts/', contacts_page, name='contacts'),
    path('faqs/', faq_view, name='faq-view'),
    path('user_profile/', user_section, name='user-profile'),

    path("", register, name="register"),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout .as_view(), name='logout'),
    path('disable_notification/', disable_notifications, name='disable-notification'),
    path('alerts/<int:id>/', get_alert, name="alert"),

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

    # Payment methods
    path('process_payment/', process_subscription, name='process-payment'),
    path('payment_done/', payment_done, name='payment-done'),
    path('payment_cancelled/', payment_canceled, name='payment-cancelled'),

    path('promo_code/', process_promo_code, name='promo-code'),

    # Account activation
    path("activation_email/", email_sent, name="email-sent"),
    re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate_account, name='activate'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
