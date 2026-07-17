from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Song, Album, Download, Genre, ListeningHistory,  PlaybackProgress
from .serializers import SongSerializer, CommentSerializer, RatingSerializer, AlbumSerializer, DownloadSerializer,GenreSerializer, ListeningHistorySerializer, PlaybackProgressSerializer
from artists.models import Artist
from rest_framework import generics
from .models import Song, PlayHistory
from django.db.models import Q, Count, F
from .models import Comment
from .models import Rating
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Sum
from subscriptions.models import Subscription
import random
from rest_framework.permissions import AllowAny
from .models import Advertisement
from rest_framework.generics import ListAPIView
from .models import RecentlyPlayed
from .serializers import RecentlyPlayedSerializer
import os
from django.db.models import Count, Sum
from accounts.permissions import IsArtist
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes


class SongUploadView(APIView):

        permission_classes = [IsAuthenticated, IsArtist]

        def post(self, request):

            try:
                artist = Artist.objects.get(user=request.user)

            except Artist.DoesNotExist:
                return Response(
                    {'error': 'Artist profile not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = SongSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(artist=artist)

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        


class SongListView(generics.ListAPIView):

        permission_classes = [AllowAny]

        queryset = Song.objects.all().order_by('-uploaded_at')

        serializer_class = SongSerializer




class LikeSongView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            song = Song.objects.get(id=pk)
        except Song.DoesNotExist:
            return Response(
                {"error": "Song not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 🔥 CHECK if already liked
        if song.liked_by.filter(id=request.user.id).exists():
            return Response(
                {"message": "Song already in favorites"},
                status=status.HTTP_400_BAD_REQUEST
            )

        song.liked_by.add(request.user)

        return Response(
            {"message": "Song added to favorites"},
            status=status.HTTP_200_OK
        )

class UnlikeSongView(APIView):

        permission_classes = [IsAuthenticated]

        def post(self, request, pk):

            try:
                song = Song.objects.get(id=pk)

            except Song.DoesNotExist:

                return Response(
                    {'error': 'Song not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            song.liked_by.remove(request.user)

            return Response(
                {'message': 'Song unliked successfully'},
                status=status.HTTP_200_OK
            )
        

class PlaySongView(APIView):

        permission_classes = [IsAuthenticated]

        def post(self, request, pk):

            try:
                song = Song.objects.get(id=pk)

            except Song.DoesNotExist:

                return Response(
                    {'error': 'Song not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            song.plays += 1
            song.save()

            # Play History
            PlayHistory.objects.create(
                user=request.user,
                song=song
            )

            # Recently Played
            RecentlyPlayed.objects.create(
                user=request.user,
                song=song
            )

            return Response(
                {'message': 'Song played successfully'},
                status=status.HTTP_200_OK
            )

class RecentlyPlayedView(generics.ListAPIView):

        serializer_class = SongSerializer

        permission_classes = [IsAuthenticated]

        def get_queryset(self):

            history = PlayHistory.objects.filter(
                user=self.request.user
            ).order_by('-played_at')

            song_ids = history.values_list(
                'song_id',
                flat=True
            )

            return Song.objects.filter(
                id__in=song_ids
            ).distinct()
        

class SongSearchView(generics.ListAPIView):

        serializer_class = SongSerializer

        def get_queryset(self):

            query = self.request.GET.get('q')

            if query:

                return Song.objects.filter(

                    Q(title__icontains=query) |

                    Q(album_name__icontains=query) |

                    Q(genre__name__icontains=query)

                )

            return Song.objects.none()
        


class RecommendedSongsView(generics.ListAPIView):

        serializer_class = SongSerializer

        permission_classes = [IsAuthenticated]

        def get_queryset(self):

            liked_songs = self.request.user.liked_songs.all()

            genres = liked_songs.values_list(
                'genre',
                flat=True
            )

            recommended_songs = Song.objects.filter(
                genre__in=genres
            ).exclude(
                liked_by=self.request.user
            ).distinct()

            return recommended_songs
        


class SongCommentView(generics.ListCreateAPIView):

        serializer_class = CommentSerializer

        permission_classes = [IsAuthenticated]

        def get_queryset(self):

            return Comment.objects.filter(
                song_id=self.kwargs['pk']
            ).order_by('-created_at')

        def perform_create(self, serializer):

            serializer.save(
                user=self.request.user,
                song_id=self.kwargs['pk']
            )



class SongRatingView(generics.ListCreateAPIView):

        serializer_class = RatingSerializer

        permission_classes = [IsAuthenticated]

        def get_queryset(self):

            return Rating.objects.filter(
                song_id=self.kwargs['pk']
            )

        def perform_create(self, serializer):

            serializer.save(
                user=self.request.user,
                song_id=self.kwargs['pk']
            )


class AverageRatingView(APIView):

        def get(self, request, pk):

            average = Rating.objects.filter(
                song_id=pk
            ).aggregate(
                Avg('stars')
            )

            return Response({
                'average_rating': average['stars__avg']
            })
        



class TrendingSongsView(generics.ListAPIView):

        serializer_class = SongSerializer

        def get_queryset(self):

            return Song.objects.all().order_by('-plays')[:10]
        



class AlbumListCreateView(generics.ListCreateAPIView):

        queryset = Album.objects.all()

        serializer_class = AlbumSerializer

        permission_classes = [IsAuthenticated]

        def perform_create(self, serializer):

            serializer.save(artist=self.request.user)



class SongDetailView(generics.RetrieveUpdateAPIView):

        queryset = Song.objects.all()

        serializer_class = SongSerializer

        permission_classes = [IsAuthenticated]



class DownloadSongView(generics.ListCreateAPIView):

        serializer_class = DownloadSerializer

        permission_classes = [IsAuthenticated]

        def get_queryset(self):

            return Download.objects.filter(
                user=self.request.user
            )

        def perform_create(self, serializer):

            serializer.save(user=self.request.user)


class GenreListCreateView(generics.ListCreateAPIView):

        queryset = Genre.objects.all()

        serializer_class = GenreSerializer

        permission_classes = [IsAuthenticated]


class SongsByGenreView(generics.ListAPIView):

        serializer_class = SongSerializer

        permission_classes = [IsAuthenticated]

        def get_queryset(self):

            genre_id = self.kwargs['genre_id']

            return Song.objects.filter(
                genre_id=genre_id
            )
        

class ClearRecentlyPlayedView(APIView):

        permission_classes = [IsAuthenticated]

        def delete(self, request):

            PlayHistory.objects.filter(
                user=request.user
            ).delete()

            return Response(
                {'message': 'Recently played cleared successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        

class AddListeningHistoryView(APIView):

        permission_classes = [IsAuthenticated]

        def post(self, request, song_id):

            song = get_object_or_404(
                Song,
                id=song_id
            )

            ListeningHistory.objects.create(
                user=request.user,
                song=song
            )

            return Response({
                "message": "Song added to history"
            })
        
class RecentlyPlayedView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            history = ListeningHistory.objects.filter(
                user=request.user
            ).order_by("-played_at")[:10]

            serializer = ListeningHistorySerializer(
                history,
                many=True
            )

            return Response(serializer.data)
        

class SavePlaybackProgressView(APIView):

        permission_classes = [IsAuthenticated]

        def post(self, request, song_id):

            song = get_object_or_404(
                Song,
                id=song_id
            )

            current_position = request.data.get(
                "current_position",
                0
            )

            completed = request.data.get(
                "completed",
                False
            )

            progress, created = PlaybackProgress.objects.update_or_create(
                user=request.user,
                song=song,

                defaults={
                    "current_position": current_position,
                    "completed": completed
                }
            )

            serializer = PlaybackProgressSerializer(progress)

            return Response(serializer.data)
        

class ContinueListeningView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            progress = PlaybackProgress.objects.filter(
                user=request.user,
                completed=False
            ).order_by("-updated_at")

            serializer = PlaybackProgressSerializer(
                progress,
                many=True
            )

            return Response(serializer.data)
        
class TopSongsAnalyticsView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            top_songs = ListeningHistory.objects.filter(
                user=request.user
            ).values(
                "song__title"
            ).annotate(
                play_count=Count("song")
            ).order_by("-play_count")[:10]

            return Response(top_songs)
        

class TopArtistsAnalyticsView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            top_artists = ListeningHistory.objects.filter(
                user=request.user
            ).values(
                "song__artist__stage_name"
            ).annotate(
                play_count=Count("song")
            ).order_by("-play_count")[:10]

            return Response(top_artists)
        

        
class ListeningSummaryView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            history = ListeningHistory.objects.filter(
                user=request.user
            )

            total_plays = history.count()

            unique_songs = history.values(
                "song"
            ).distinct().count()

            total_listening_time = history.count() * 3

            return Response({

                "total_plays": total_plays,

                "unique_songs": unique_songs,

                "estimated_listening_minutes":
                total_listening_time
            })
        

class SpotifyWrappedView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            history = ListeningHistory.objects.filter(
                user=request.user
            )

            total_plays = history.count()

            total_minutes = total_plays * 3

            unique_songs = history.values(
                "song"
            ).distinct().count()

            top_song = history.values(
                "song__title"
            ).annotate(
                play_count=Count("song")
            ).order_by("-play_count").first()

            top_artist = history.values(
                "song__artist__stage_name"
            ).annotate(
                play_count=Count("song")
            ).order_by("-play_count").first()

            return Response({

                "total_plays": total_plays,

                "total_minutes":
                total_minutes,

                "unique_songs":
                unique_songs,

                "top_song":
                top_song,

                "top_artist":
                top_artist,
            })
        

class StreamSongView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request, song_id):

            song = get_object_or_404(
                Song,
                id=song_id
            )

            ads_enabled = True

            subscription = Subscription.objects.filter(
                user=request.user
            ).first()

            song.stream_count = F("stream_count") + 1
            song.save()

            song.refresh_from_db()

            # Listening History
            ListeningHistory.objects.create(
                user=request.user,
                song=song
            )

            # Recently Played
            RecentlyPlayed.objects.create(
                user=request.user,
                song=song
            )

            if subscription and subscription.can_use_ad_free():
                ads_enabled = False

            ad_data = None

            if ads_enabled:

                ads = Advertisement.objects.filter(
                    active=True
                )

                if ads.exists():

                    random_ad = random.choice(list(ads))

                    ad_data = {
                        "title": random_ad.title,
                        "ad_type": random_ad.ad_type,
                        "media_file": random_ad.media_file.url if random_ad.media_file else None
                    }

            return Response({

                "song_id": song.id,
                "song_title": song.title,
                "artist": song.artist.stage_name,
                "audio_url": song.audio_file.url,
                "stream_count": song.stream_count,
                "advertisement": ad_data
            })
        

class RecommendationView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            favorite_genre = ListeningHistory.objects.filter(
                user=request.user
            ).values(
                "song__genre__name"
            ).annotate(
                total=Count("song")
            ).order_by("-total").first()

            if not favorite_genre:

                return Response({
                    "message": "No listening history found"
                })

            genre_name = favorite_genre["song__genre__name"]

            recommended_songs = Song.objects.filter(
                genre__name=genre_name
            ).order_by("-stream_count")[:10]

            data = []

            for song in recommended_songs:

                data.append({

                    "id": song.id,

                    "title": song.title,

                    "artist": song.artist.stage_name,

                    "genre": song.genre.name
                    if song.genre else None,

                    "stream_count": song.stream_count,
                })

            return Response(data)
        

class TrendingRecommendationView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            songs = Song.objects.order_by(
                "-stream_count"
            )[:10]

            data = []

            for song in songs:

                data.append({

                    "id": song.id,

                    "title": song.title,

                    "artist": song.artist.stage_name,

                    "stream_count": song.stream_count,
                })

            return Response(data)
        

class GenreRecommendationView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request, genre):

            songs = Song.objects.filter(
                genre__name__iexact=genre
            ).order_by("-stream_count")[:10]

            data = []

            for song in songs:

                data.append({

                    "id": song.id,

                    "title": song.title,

                    "artist": song.artist.stage_name,

                    "genre": song.genre.name
                    if song.genre else None,
                })

            return Response(data)
        

class AdminDashboardView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            if not request.user.is_staff:

                return Response({
                    "error": "Admin access only"
                }, status=403)

            User = get_user_model()

            total_users = User.objects.count()

            total_songs = Song.objects.count()

            total_streams = Song.objects.aggregate(
            total=Count("plays")
            )

            total_artists = Artist.objects.count()

            return Response({

                "total_users": total_users,

                "total_songs": total_songs,

                "total_artists": total_artists,

                "total_streams":
                total_streams["total"],
            })
        

class AdminTopSongsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_staff:
            return Response({"error": "Admin access only"}, status=403)

        songs = Song.objects.all().order_by("-plays")

        serializer = SongSerializer(songs, many=True)

        return Response(serializer.data)
        

class AdminTopArtistsView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            if not request.user.is_staff:

                return Response({
                    "error": "Admin access only"
                }, status=403)

            artists = Artist.objects.annotate(
            total_streams=Sum("songs__plays")
            ).order_by("-total_streams")[:10]

            data = []
            for artist in artists:

                data.append({

                    "id": artist.id,

                    "artist": artist.stage_name,

                    "total_streams": artist.total_streams or 0

                })

            return Response(data)
        

class AdminArtistSongsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, artist_id):

        songs = Song.objects.filter(
            artist_id=artist_id
        )

        serializer = SongSerializer(
            songs,
            many=True
        )

        return Response(serializer.data)
    


class PremiumSongDownloadView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request, song_id):

            subscription = Subscription.objects.get(
                user=request.user
            )

            # Premium access check
            if not subscription.can_download():

                return Response({

                    "error":
                    "Premium subscription required"

                }, status=403)

            song = get_object_or_404(
                Song,
                id=song_id
            )

            return Response({

                "message":
                "Download access granted",

                "song": song.title,

                "download_url":
                song.audio_file.url
            })
        

class MusicUploadView(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
            print("POST DATA:", request.POST)
            print("FILES:", request.FILES)

            serializer = SongSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            print("ERRORS:", serializer.errors)
            return Response(serializer.errors, status=400)
        


class RecentlyPlayedView(ListAPIView):
        serializer_class = RecentlyPlayedSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self):
            return RecentlyPlayed.objects.filter(
                user=self.request.user
            )
        

class BulkUploadSongsView(APIView):

        permission_classes = [IsAuthenticated]

        def post(self, request):

            files = request.FILES.getlist("audio_files")

            genre_id = request.data.get("genre")
            album_id = request.data.get("album")

            genre = Genre.objects.filter(id=genre_id).first()
            album = Album.objects.filter(id=album_id).first()

            uploaded_songs = []

            for file in files:

                title = os.path.splitext(file.name)[0]
                title = title.replace("-", " ")
                title = title.replace("_", " ")

                song = Song.objects.create(
                    title=title,
                    audio_file=file,
                    artist=request.user.artist,
                    genre=genre,
                    album=album
                )

                uploaded_songs.append({
                    "id": song.id,
                    "title": song.title,
                    "genre": genre.name if genre else None,
                    "album": album.title if album else None
                })

            return Response(
                {
                    "message": f"{len(uploaded_songs)} songs uploaded",
                    "songs": uploaded_songs
                },
                status=201
            )
        


class ArtistDashboardView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            try:
                artist = Artist.objects.get(user=request.user)

            except Artist.DoesNotExist:

                return Response(
                    {"error": "Artist profile not found"},
                    status=404
                )

            songs = Song.objects.filter(artist=artist)

            total_songs = songs.count()

            total_plays = songs.aggregate(
                total=Sum("plays")
            )["total"] or 0

            return Response({

                "artist": artist.stage_name,

                "followers": artist.followers.count(),

                "total_songs": total_songs,

                "total_plays": total_plays
    })
        

class ArtistTopSongsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            artist = Artist.objects.get(user=request.user)
        except Artist.DoesNotExist:
            return Response({"error": "Artist profile not found"}, status=404)

        songs = Song.objects.filter(artist=artist).order_by("-plays")[:10]
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


class ArtistRecentUploadsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            artist = Artist.objects.get(user=request.user)
        except Artist.DoesNotExist:
            return Response({"error": "Artist profile not found"}, status=404)

        songs = Song.objects.filter(artist=artist).order_by("-uploaded_at")[:10]
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
        

class ArtistFollowersAnalyticsView(APIView):

        permission_classes = [IsAuthenticated]

        def get(self, request):

            artist = Artist.objects.get(
                user=request.user
            )

            return Response({

                "artist": artist.stage_name,

                "followers": artist.followers,

                "verified": artist.verified
            })
        


        
class FavoriteSongsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        songs = request.user.liked_songs.all()

        serializer = SongSerializer(
            songs,
            many=True
        )

        return Response(serializer.data)
    


class SongUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            song = Song.objects.get(id=pk)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"},
                status=404
            )

        title = request.data.get("title")

        if title:
            song.title = title
            song.save()

        return Response(
            {"message": "Song updated successfully"}
        )


class SongDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            song = Song.objects.get(id=pk)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"},
                status=404
            )

        song.delete()

        return Response(
            {"message": "Song deleted successfully"}
        )
    
User = get_user_model()

class TopUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        print("🔥 TOP USERS API CALLED")
        users = User.objects.all().order_by("-date_joined")[:10]

        data = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
            }
            for u in users
        ]

        return Response(data)
