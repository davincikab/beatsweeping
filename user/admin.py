from django.contrib import admin
from .models import CustomUser, UserProfile, CouponCode, Alert

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'subscription_id')
    list_filter = ['is_active', 'is_staff']
    search_fields = ('email', 'username')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'section_name', 'is_subscribed', 'phone_number', 'disabled')
    list_filter = ('is_subscribed', 'one_hour', 'twelve_hours', 'email_notification', 'disabled')
    search_fields = ('email', 'section_name', 'name')
    ordering = ('email', '-is_subscribed')

@admin.register(CouponCode)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'isUsed', 'expiresOn')
    list_filter = ['isUsed']
    search_fields = ['code']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('user_id',)