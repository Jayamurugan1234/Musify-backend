from rest_framework import serializers
from .models import CustomUser, Follow
from playlists.models import Playlist
from playlists.serializers import PlaylistSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        role = validated_data.get('role', 'user')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )

        return user
    


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        fields = [
            'id',
            'username',
            'email',
            'role',
            'bio',
            'profile_image',
            "favorite_genre",
        ]
        


class FollowSerializer(serializers.ModelSerializer):

    class Meta:

        model = Follow

        fields = '__all__'

        read_only_fields = ['follower']




class UserProfileSerializer(serializers.ModelSerializer):

    followers_count = serializers.SerializerMethodField()

    following_count = serializers.SerializerMethodField()

    playlists_count = serializers.SerializerMethodField()

    public_playlists = serializers.SerializerMethodField()

    class Meta:

        model = CustomUser

        fields = [
            'id',
            'username',
            'email',
            'followers_count',
            'following_count',
            'playlists_count',
            'public_playlists'
        ]

    def get_followers_count(self, obj):

        return obj.followers.count()

    def get_following_count(self, obj):

        return obj.following.count()

    def get_playlists_count(self, obj):

        return obj.playlists.count()

    def get_public_playlists(self, obj):

        playlists = Playlist.objects.filter(
            user=obj,
            is_public=True
        )

        return PlaylistSerializer(
            playlists,
            many=True
        ).data
    

class PublicProfileSerializer(serializers.ModelSerializer):

    followers_count = serializers.SerializerMethodField()

    following_count = serializers.SerializerMethodField()


    class Meta:

        model = CustomUser
        fields = [
            "id",
            "username",
            "bio",
            "profile_image",
            "favorite_genre",
            "followers_count",
            "following_count",
        ]


    def get_followers_count(self, obj):

        return obj.followers.count()


    def get_following_count(self, obj):

        return obj.following.count()