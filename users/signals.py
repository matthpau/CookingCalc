# from django.contrib.auth.models import User  # Standard User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # equivalent to a = Profile(user=instance), a.save()

# Prevent recursion
# https://stackoverflow.com/questions/10840030/django-post-save-preventing-recursion-without-overriding-model-save
