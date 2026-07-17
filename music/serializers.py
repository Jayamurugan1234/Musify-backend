from rest_framework import serializers
from .models import Song, Album, Download, Genre
from .models import Comment, ListeningHistory, PlaybackProgress
from .models import Rating
from .models import RecentlyPlayed

class SongSerializer(serializers.ModelSerializer):

    artist_name = serializers.CharField(
        source="artist.stage_name",
        read_only=True
    )

    class Meta:
        model = Song

        fields = '__all__'
        read_only_fields = ["artist", "created_at"]



class CommentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Comment

        fields = '__all__'

        read_only_fields = ['user', 'song']


class RatingSerializer(serializers.ModelSerializer):

    class Meta:

        model = Rating

        fields = '__all__'

        read_only_fields = ['user', 'song']



class AlbumSerializer(serializers.ModelSerializer):

    class Meta:

        model = Album

        fields = '__all__'

        read_only_fields = ['artist']


class DownloadSerializer(serializers.ModelSerializer):

    class Meta:

        model = Download

        fields = '__all__'

        read_only_fields = ['user']



class GenreSerializer(serializers.ModelSerializer):

    class Meta:

        model = Genre

        fields = '__all__'

class ListeningHistorySerializer(serializers.ModelSerializer):

    song_title = serializers.CharField(
        source="song.title",
        read_only=True
    )

    artist = serializers.CharField(
        source="song.artist.username",
        read_only=True
    )

    class Meta:

        model = ListeningHistory

        fields = [
            "id",
            "song",
            "song_title",
            "artist",
            "played_at",
        ]



class PlaybackProgressSerializer(serializers.ModelSerializer):

    song_title = serializers.CharField(
        source="song.title",
        read_only=True
    )

    class Meta:

        model = PlaybackProgress

        fields = [
            "id",
            "song",
            "song_title",
            "current_position",
            "completed",
            "updated_at",
        ]




class RecentlyPlayedSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)

    class Meta:
        model = RecentlyPlayed
        fields = "__all__"
