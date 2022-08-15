from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def pre_save_handler(sender, instance, *args, **kwargs):
    if not isinstance(instance, Session):
        instance.full_clean()
    pass
