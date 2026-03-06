# apps/approved/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.approved.models import Approved
from apps.progress.models import Progress

@receiver(post_save, sender=Approved)
def create_progress_on_approval(sender, instance, created, **kwargs):
    if created:
        Progress.objects.get_or_create(application=instance.application)
