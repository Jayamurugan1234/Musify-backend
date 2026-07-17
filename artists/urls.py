from django.urls import path

from .views import (
    ArtistListCreateView,
    FollowArtistView,
    UnfollowArtistView
)

urlpatterns = [

    path(
        '',
        ArtistListCreateView.as_view(),
        name='artist-list-create'
    ),

    path(
        '<int:pk>/follow/',
        FollowArtistView.as_view(),
        name='follow-artist'
    ),

    path(
        '<int:pk>/unfollow/',
        UnfollowArtistView.as_view(),
        name='unfollow-artist'
    ),
]