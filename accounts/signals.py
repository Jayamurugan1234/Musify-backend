from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_artist_profile(sender, instance, created, **kwargs):
    """
    Whenever a CustomUser is created with role='artists',
    automatically create a matching Artist row linked to them.
    Runs on every save, but only acts on first creation to avoid
    duplicate Artist rows on later profile edits.
    """
    if not created:
        return

    if instance.role != 'artists':
        return

    # Import here (not at top) to avoid circular import issues
    # since artists app may import from accounts app too.
    from artists.models import Artist

    Artist.objects.get_or_create(
        user=instance,
        defaults={'stage_name': instance.username}
    )
