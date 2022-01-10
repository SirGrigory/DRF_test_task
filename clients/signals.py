from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Client, Profile


@receiver(post_save, sender = Client)
def profile_create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)
    