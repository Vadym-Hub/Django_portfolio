import os

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver


User = get_user_model()


@receiver(pre_save, sender=User)
def post_update(sender, instance, **kwargs):
    """
    Удаление старого аватара после обновления.
    """
    if not instance.pk:
        return False

    if sender.objects.get(pk=instance.pk).avatar:
        old_avatar = sender.objects.get(pk=instance.pk).avatar
        new_avatar = instance.avatar
        if not old_avatar == new_avatar:
            if os.path.isfile(old_avatar.path):
                os.remove(old_avatar.path)
    else:
        return False
