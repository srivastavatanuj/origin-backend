# your_app/signals.py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ClientCataloge
from django.db import transaction


# @receiver(post_save, sender=User)
# def create_catalog_for_superuser(sender, instance, created, **kwargs):
#     print(12)
#     if instance.is_superuser and not ClientCataloge.objects.exists():
#         ClientCataloge.objects.create(name="Default", user=instance)
