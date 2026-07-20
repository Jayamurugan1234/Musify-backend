from django.db import models
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from artists.models import Artist
from accounts.models import CustomUser
from django.conf import settings

class Song(models.Model):

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='songs'
    )

    title = models.CharField(max_length=255)

    album = models.ForeignKey(
        'Album',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='songs'
    )

    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='songs'
    )

    cover_image = models.URLField(max_length=500, blank=True, null=True)

    audio_file = models.FileField(
        upload_to='songs/',
        storage=VideoMediaCloudinaryStorage(),
    )

    lyrics = models.TextField(blank=True, null=True)

    duration = models.DurationField(blank=True, null=True)

    plays = models.PositiveIntegerField(default=0)

    liked_by = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='liked_songs'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class PlayHistory(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='play_history'
    )

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='play_history'
    )

    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} played {self.song.title}"
    

class Comment(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} - {self.song.title}"
    

class Rating(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    stars = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} rated {self.song.title}"
    


class Album(models.Model):

    artist = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)

    cover_image = models.ImageField(
        upload_to='albums/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title
    


class Download(models.Model):

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE
    )

    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} downloaded {self.song.title}"
    


class Genre(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):

        return self.name
    

class ListeningHistory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    song = models.ForeignKey(
        "Song",
        on_delete=models.CASCADE
    )

    played_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} played {self.song.title}"
    

class PlaybackProgress(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    song = models.ForeignKey(
        "Song",
        on_delete=models.CASCADE
    )

    current_position = models.IntegerField(
        default=0
    )

    completed = models.BooleanField(
        default=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.song.title}"
    


class Advertisement(models.Model):

    AD_TYPES = (

        ('audio', 'Audio'),

        ('banner', 'Banner'),
    )

    title = models.CharField(
        max_length=255
    )

    ad_type = models.CharField(
        max_length=20,
        choices=AD_TYPES
    )

    media_file = models.URLField()

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title
    


class RecentlyPlayed(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    song = models.ForeignKey(
        "music.Song",
        on_delete=models.CASCADE
    )

    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-played_at"]

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"

