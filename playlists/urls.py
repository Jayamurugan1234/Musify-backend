from django.urls import path
from .views import PlaylistCreateView
from .views import (
    PlaylistCreateView,
    AddSongToPlaylistView,
    RemoveSongFromPlaylistView,
    AddCollaboratorView, ReorderPlaylistView, PlaylistSongReorderView, PlaylistReorderView, LikePlaylistView, UnlikePlaylistView,PlaylistDetailView,PlaylistDeleteView,
)
print("🔥 PLAYLIST URLS LOADED")

urlpatterns = [
    

    path('', PlaylistCreateView.as_view(), name='playlist-list-create'),


    path('<int:pk>/add-song/', AddSongToPlaylistView.as_view()),
    
    path('<int:pk>/remove-song/',RemoveSongFromPlaylistView.as_view(),name='remove-song-from-playlist'),


    path('<int:pk>/add-collaborator/',AddCollaboratorView.as_view(),name='add-collaborator'),


    path('reorder/',ReorderPlaylistView.as_view(),name='playlist-reorder'),


    path('reorder/<int:pk>/',PlaylistSongReorderView.as_view(),name='playlist-reorder'),


    path('<int:pk>/reorder/',PlaylistReorderView.as_view(),name='playlist-reorder'),


    path('<int:pk>/like/',LikePlaylistView.as_view(),name='playlist-like'),

    
    path('<int:pk>/unlike/',UnlikePlaylistView.as_view(),name='playlist-unlike'),


    path("<int:pk>/", PlaylistDetailView.as_view()),


    path("<int:pk>/delete/",PlaylistDeleteView.as_view(),name="playlist-delete"),


]



