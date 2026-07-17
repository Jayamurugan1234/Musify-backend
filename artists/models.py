from django.db import models
from accounts.models import CustomUser
from accounts.models import CustomUser
from django.conf import settings

class Artist(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    stage_name = models.CharField(max_length=200)

    cover_image = models.ImageField(
        upload_to='artist_covers/',
        blank=True,
        null=True
    )

    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="followed_artists"
    )

    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
    

