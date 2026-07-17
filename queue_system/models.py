from django.db import models
from accounts.models import CustomUser
from music.models import Song


class Queue(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='queues'
    )

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ['added_at']

    def __str__(self):

        return f"{self.user.username} - {self.song.title}"