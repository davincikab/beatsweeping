from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils import timezone

import uuid

class CustomUser(AbstractUser):
    SMS_TIME = (
        ('Y', 'Yes'),
        ('N', 'No')
    )
    username = models.CharField("Username", max_length=50, unique=True)
    email = models.EmailField("Email", max_length=254, unique=True)
    is_subscribed = models.CharField("Subscription", default='N', max_length=5, choices=SMS_TIME)
    disabled_notification = models.CharField("Notification", max_length=50, default='N')
    subscription_id = models.CharField(_("Subscription ID"), max_length=50, null=True)
    subscription_date = models.DateField("Subscription Date", blank=True, null=True)
    bounds = models.CharField("Bounds", max_length=100)

    USER_NAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
# Create your models here.
class UserProfile(models.Model):
    # options
    SMS_TIME = (
        ('Y', 'Yes'),
        ('N', 'No')
    )

    user_id = models.IntegerField(_("User Id"), blank=True, null=True)
    section_name = models.CharField("Section Name", max_length=100, null=False)
    oid = models.IntegerField("Object Id", blank= False)
    name = models.CharField("Name", max_length=50, blank=True, null=True)
    phone_number = models.CharField('Phone Number', max_length=13, blank=True)
    email = models.EmailField("Email", unique=False)
    twelve_hours = models.CharField("Twelve hours", max_length=5, choices=SMS_TIME, default='Y')
    one_hour = models.CharField("One hour", max_length=5,choices=SMS_TIME, default='Y')
    is_subscribed = models.CharField("Subscription", default='N', max_length=5, choices=SMS_TIME)
    subscription_date = models.DateField("Subscription Date", blank=True, null=True)
    subscription_duration = models.IntegerField("Subscription Duration", blank=True, null=True)
    date_registered = models.DateTimeField("Date Registered", auto_now=True)
    disabled = models.CharField(_("Notification"), max_length=50, default='N')
    email_notification = models.CharField(_("Email Notification"), max_length=5, choices=SMS_TIME, default="N")

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        return self.email

# Coupon Code;
class CouponCode(models.Model):
    code = models.CharField("Coupon Code", max_length=5, unique=True)
    isUsed = models.BooleanField("Is Used", default=False)
    expiresOn = models.DateTimeField("Expires On", auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = _("CouponCode")
        verbose_name_plural = _("CouponCodes")

    def __str__(self):
        return self.code

class Alert(models.Model):
    user_id = models.IntegerField("User Id", unique=True) 

    class Meta:
        verbose_name = _("Alert")
        verbose_name_plural = _("Alerts")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Alert_detail", kwargs={"pk": self.pk})