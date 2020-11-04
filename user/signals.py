from django.core.mail import EmailMessage
from django.db.models.signals import post_save, post_delete

from .models import UserProfile, CustomUser
from datetime import datetime
from django.dispatch import receiver


# user preregistry signals
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, **kwargs):
    print(sender)
    print("iNSTANCE")
    print(instance.is_subscribed)
    sections = UserProfile.objects.filter(email = instance.email)

    for section in sections:
        section.is_subscribed = instance.is_subscribed
        section.subscription_date = datetime.now()
        section.subscription_duration = 1

        section.save()


@receiver(post_delete, sender=CustomUser)
def delete_related_user_instances(sender, instance, **kwargs):
    # delete userprofile
    print(instance)
    profiles = UserProfile.objects.filter(email = instance.email)
    print(profiles)
    if profiles:
        for profile in profiles:
            profile.delete()
