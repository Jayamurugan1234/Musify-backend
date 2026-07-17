from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Artist
from .serializers import ArtistSerializer


class ArtistListCreateView(generics.ListCreateAPIView):

    queryset = Artist.objects.all()

    serializer_class = ArtistSerializer


class FollowArtistView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            artist = Artist.objects.get(id=pk)

        except Artist.DoesNotExist:

            return Response(
                {'error': 'Artist not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        artist.followers.add(request.user)

        return Response(
            {'message': 'Artist followed successfully'},
            status=status.HTTP_200_OK
        )


class UnfollowArtistView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            artist = Artist.objects.get(id=pk)

        except Artist.DoesNotExist:

            return Response(
                {'error': 'Artist not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        artist.followers.remove(request.user)

        return Response(
            {'message': 'Artist unfollowed successfully'},
            status=status.HTTP_200_OK
        )