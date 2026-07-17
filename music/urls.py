from django.urls import path
from .views import SongUploadView
from .views import (
    SongUploadView,
    SongListView,
    LikeSongView,
    UnlikeSongView,
    PlaySongView,
    RecentlyPlayedView,
    SongSearchView,
    RecommendedSongsView,
    SongCommentView,
    SongRatingView,
    AverageRatingView,
    TrendingSongsView,
    AlbumListCreateView,
    SongDetailView,
    DownloadSongView,
    GenreListCreateView,
    SongsByGenreView,
    ClearRecentlyPlayedView,
    AddListeningHistoryView,
    SavePlaybackProgressView,
    ContinueListeningView,
    TopSongsAnalyticsView,
    TopArtistsAnalyticsView,
    ListeningSummaryView,
    SpotifyWrappedView,
    StreamSongView,
    RecommendationView,
    TrendingRecommendationView,
    GenreRecommendationView,
    AdminDashboardView,
    AdminTopSongsView,
    AdminTopArtistsView,
    PremiumSongDownloadView,
    MusicUploadView,
    RecentlyPlayedView,
   
    ArtistDashboardView,
    ArtistTopSongsView,
    ArtistRecentUploadsView,
    ArtistFollowersAnalyticsView,
    FavoriteSongsView,
    SongUpdateView,
    SongDeleteView,
    AdminArtistSongsView,
    TopUsersView

)


urlpatterns = [

    path('upload/', SongUploadView.as_view()),

    path('songs/', SongListView.as_view(), name='song-list'),

    path('songs/<int:pk>/like/',LikeSongView.as_view(),name='like-song'),

    path('songs/<int:pk>/unlike/',UnlikeSongView.as_view(),name='unlike-song'),

    path('songs/<int:pk>/play/',PlaySongView.as_view(),name='play-song'),

    path('recently-played/',RecentlyPlayedView.as_view(),name='recently-played'),

    path('search/',SongSearchView.as_view(),name='song-search'),

    path('recommended/',RecommendedSongsView.as_view(),name='recommended-songs'),

    path('songs/<int:pk>/comments/',SongCommentView.as_view(),name='song-comments'),

    path('songs/<int:pk>/ratings/',SongRatingView.as_view(),name='song-ratings'),

    path('songs/<int:pk>/average-rating/',AverageRatingView.as_view(),name='average-rating'),

    path('trending/',TrendingSongsView.as_view(),name='trending-songs'),

    path('albums/',AlbumListCreateView.as_view(),name='albums'),

    path('songs/<int:pk>/',SongDetailView.as_view(),name='song-detail'),

    path('downloads/',DownloadSongView.as_view(),name='downloads'),

    path('genres/',GenreListCreateView.as_view(),name='genres'),

    path('genres/<int:genre_id>/songs/',SongsByGenreView.as_view(),name='songs-by-genre'),

    path('recently-played/clear/',ClearRecentlyPlayedView.as_view(),name='clear-recently-played'),

    path("history/<int:song_id>/",AddListeningHistoryView.as_view()),

    path("save-progress/<int:song_id>/",SavePlaybackProgressView.as_view()),

    path("continue-listening/",ContinueListeningView.as_view()),

    path("analytics/top-songs/",TopSongsAnalyticsView.as_view()),

    path("analytics/top-artists/",TopArtistsAnalyticsView.as_view()),

    path("analytics/summary/",ListeningSummaryView.as_view()),

    path("wrapped/",SpotifyWrappedView.as_view()),

    path("stream/<int:song_id>/",StreamSongView.as_view()),

    path("recommendations/",RecommendationView.as_view()),

    path("trending-recommendations/",TrendingRecommendationView.as_view()),

    path("genre-recommendations/<str:genre>/",GenreRecommendationView.as_view()),

    path("admin/dashboard/",AdminDashboardView.as_view()),

    path("admin/top-songs/",AdminTopSongsView.as_view()),

    path("admin/top-artists/",AdminTopArtistsView.as_view()),

    path("premium-download/<int:song_id>/",PremiumSongDownloadView.as_view()),

    # path("upload/", MusicUploadView.as_view()),

    path("history/",RecentlyPlayedView.as_view()),

   

    path("artist/dashboard/",ArtistDashboardView.as_view()),

    path("artist/top-songs/",ArtistTopSongsView.as_view()),

    path("artist/recent-uploads/",ArtistRecentUploadsView.as_view()),

    path("artist/followers/",ArtistFollowersAnalyticsView.as_view()),

    path("favorites/",FavoriteSongsView.as_view(),name="favorite-songs"),

    path("songs/<int:pk>/update/",SongUpdateView.as_view()),

    path("songs/<int:pk>/delete/",SongDeleteView.as_view()),

    path("admin/artist-songs/<int:artist_id>/",AdminArtistSongsView.as_view()),


     path("admin/top-users/", TopUsersView.as_view()),

]


