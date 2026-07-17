from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Playlist
from .serializers import PlaylistSerializer, PlaylistSongSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.models import CustomUser
from music.models import Song
from .models import PlaylistSong
from music.models import Song
from django.db import connection
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import DestroyAPIView
from django.shortcuts import get_object_or_404



print("🔥 PLAYLIST VIEWS LOADED")

class PlaylistCreateView(generics.ListCreateAPIView):

    serializer_class = PlaylistSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Playlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class PlaylistDetailView(RetrieveAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer




    


# class AddSongToPlaylistView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):

#         try:
#             playlist = Playlist.objects.get(
#                 id=pk,
#                 user=request.user
#             )

#         except Playlist.DoesNotExist:

#             return Response(
#                 {'error': 'Playlist not found'},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         song_id = request.data.get('song_id')

#         if not song_id:
#             return Response(
#                 {'error': 'song_id required'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:
#             song = Song.objects.get(id=int(song_id))

#         except Song.DoesNotExist:

#             return Response(
#                 {'error': 'Song not found'},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         PlaylistSong.objects.get_or_create(
#             playlist=playlist,
#             song=song
#         )

#         return Response(
#             {'message': 'Song added successfully'},
#             status=status.HTTP_200_OK
#         )





# class AddSongView(APIView):
#     def post(self, request, pk):
#         playlist = Playlist.objects.get(id=pk)
#         song_id = request.data.get("song_id")

#         song = Song.objects.get(id=song_id)
#         playlist.songs.add(song)

#         return Response({"message": "Song added successfully"})
    

class AddSongToPlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        print("🔥 ADD SONG HIT")
        print("User:", request.user)
        print("Playlist ID:", pk)
        print("Body:", request.data)

        # check playlist WITHOUT user filter first (DEBUG)
        try:
            playlist = Playlist.objects.get(id=pk)

            print("REQUEST USER:", request.user.id)
            print("PLAYLIST OWNER:", playlist.user.id)
        except Playlist.DoesNotExist:
            return Response({"message": "Playlist not found"}, status=404)

        # now check ownership
        if playlist.user != request.user:
            return Response({"message": "Not your playlist"}, status=403)

        song_id = request.data.get("song_id")

        if not song_id:
            return Response({"message": "song_id missing"}, status=400)

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({"message": "Song not found"}, status=404)

        obj, created = PlaylistSong.objects.get_or_create(
            playlist=playlist,
            song=song
        )

        if not created:
            return Response({"message": "Already in playlist"}, status=400)

        return Response({"message": "Song added successfully"}, status=200)

class RemoveSongFromPlaylistView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            playlist = Playlist.objects.get(
                id=pk,
                user=request.user
            )
        except Playlist.DoesNotExist:
            return Response(
                {'error': 'Playlist not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ FIXED LINE
        song_id = request.data.get('song_id')

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {'error': 'Song not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        playlist.songs.remove(song)

        return Response(
            {'message': 'Song removed from playlist'},
            status=status.HTTP_200_OK
        )
class AddCollaboratorView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:

            playlist = Playlist.objects.get(id=pk)

        except Playlist.DoesNotExist:

            return Response(
                {'error': 'Playlist not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        user_id = request.data.get('user')

        try:

            user = CustomUser.objects.get(id=user_id)

        except CustomUser.DoesNotExist:

            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        playlist.collaborators.add(user)

        return Response({
            'message': 'Collaborator added successfully'
        })
    



class ReorderPlaylistView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        items = request.data.get('items', [])

        for item in items:

            try:

                playlist_song = Playlist.objects.get(
                    id=item['id']
                )

                playlist_song.order = item['order']

                playlist_song.save()

            except Playlist.DoesNotExist:

                pass

        return Response(
            {'message': 'Playlist reordered successfully'},
            status=status.HTTP_200_OK
        )
    

class PlaylistSongReorderView(generics.UpdateAPIView):

    queryset = PlaylistSong.objects.all()

    serializer_class = PlaylistSongSerializer


class PlaylistReorderView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        playlist_song_id = request.data.get('playlist_song_id')

        new_order = request.data.get('order')

        try:

            playlist_song = PlaylistSong.objects.get(
                id=playlist_song_id,
                playlist_id=pk
            )

        except PlaylistSong.DoesNotExist:

            return Response(
                {'error': 'Playlist song not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        playlist_song.order = new_order

        playlist_song.save()

        return Response({
            'message': 'Playlist reordered successfully'
        })
    
class LikePlaylistView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            playlist = Playlist.objects.get(id=pk)

        except Playlist.DoesNotExist:

            return Response(
                {'error': 'Playlist not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        playlist.liked_by.add(request.user)

        playlist.likes_count = playlist.liked_by.count()

        playlist.save()

        return Response({
            'message': 'Playlist liked successfully'
        })
    

class UnlikePlaylistView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            playlist = Playlist.objects.get(id=pk)

        except Playlist.DoesNotExist:

            return Response(
                {'error': 'Playlist not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        playlist.liked_by.remove(request.user)

        playlist.likes_count = playlist.liked_by.count()

        playlist.save()

        return Response({
            'message': 'Playlist unliked successfully'
        })
    



class PlaylistDeleteView(DestroyAPIView):

    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)