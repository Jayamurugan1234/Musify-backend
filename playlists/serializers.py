# from rest_framework import serializers
# from .models import Playlist, PlaylistSong
# from music.serializers import SongSerializer

# class PlaylistSongSerializer(serializers.ModelSerializer):

#     song = SongSerializer(read_only=True)
#     class Meta:

#         model = PlaylistSong

#         fields = ['id', 'song', 'order','added_at']


# class PlaylistSerializer(serializers.ModelSerializer):

#     playlist_songs = PlaylistSongSerializer(
#         source='playlistsong_set',
#         many=True,
#         read_only=True
#     )

#     class Meta:

#         model = Playlist

#         fields = [
#             'id',
#             'name',
#             'user',
#             'playlist_songs',
#             'is_public',
#             'likes_count',
#             'liked_by',
#             'created_at'
#         ]





from rest_framework import serializers
from .models import Playlist, PlaylistSong
from music.serializers import SongSerializer


class PlaylistSongSerializer(serializers.ModelSerializer):

    song = SongSerializer(read_only=True)

    class Meta:
        model = PlaylistSong
        fields = [
            "id",
            "song",
            "order",
            "added_at"
        ]


class PlaylistSerializer(serializers.ModelSerializer):

    playlist_songs = PlaylistSongSerializer(
        source="playlistsong_set",
        many=True,
        read_only=True
    )

    class Meta:
        model = Playlist

        fields = [
            "id",
            "name",
            "user",
            "playlist_songs",
            "is_public",
            "likes_count",
            "liked_by",
            "created_at"
        ]

        read_only_fields = [
            "user",
            "playlist_songs",
            "likes_count",
            "liked_by",
            "created_at"
        ]