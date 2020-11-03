from django.core.mail import EmailMessage
from django.db.models.signals import post_save, post_delete

from .models import UserProfile, CustomUser
from datetime import datetime
from django.dispatch import receiver

@receiver(post_delete, sender=CustomUser)
def delete_related_user_instances(sender, instance, **kwargs):
    # delete userprofile
    print(instance)
    profiles = UserProfile.objects.filter(email = instance.email)
    print(profiles)
    if profiles:
        for profile in profiles:
            profile.delete()
