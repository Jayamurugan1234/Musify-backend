from django.db import models
from accounts.models import CustomUser
from music.models import Song


class Playlist(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='playlists'
    )

    name = models.CharField(max_length=255)

    songs = models.ManyToManyField(
    Song,
    through='PlaylistSong'
    )

    order = models.PositiveIntegerField(default=0)

    is_public = models.BooleanField(default=True)

    liked_by = models.ManyToManyField(
    CustomUser,
    blank=True,
    related_name='liked_playlists'
)

    likes_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


    collaborators = models.ManyToManyField(
    CustomUser,
    blank=True,
    related_name='collaborative_playlists'
    )


class PlaylistSong(models.Model):

    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE
    )

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ['order']

    def __str__(self):

        return f"{self.playlist.name} - {self.song.title}"