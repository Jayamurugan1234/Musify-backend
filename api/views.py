from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from accounts.models import CustomUser
from music.models import Song, PlayHistory
from playlists.models import Playlist



class AdminDashboardView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        total_users = CustomUser.objects.count()

        total_songs = Song.objects.count()

        total_playlists = Playlist.objects.count()

        total_plays = PlayHistory.objects.count()

        premium_users = CustomUser.objects.filter(
            subscription__plan='premium'
        ).count()

        return Response({

            'total_users': total_users,

            'total_songs': total_songs,

            'total_playlists': total_playlists,

            'total_plays': total_plays,

            'premium_users': premium_users
        })