from django.urls import path
from .views import RegisterView
from .views import RegisterView, ProfileView, FollowUserView, UserProfileView, PublicProfileView,  FollowUserView, UnfollowUserView, FollowersListView, FollowingListView, ForgotPasswordView, ResetPasswordView



urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('follow/',FollowUserView.as_view(),name='follow-user'),

    path('profile/<int:pk>/',UserProfileView.as_view(),name='user-profile'),

    path("users/<str:username>/",PublicProfileView.as_view()),

    path("follow/<str:username>/",FollowUserView.as_view()),

    path("unfollow/<str:username>/",UnfollowUserView.as_view()),

    path("followers/<str:username>/",FollowersListView.as_view()),

    path("following/<str:username>/",FollowingListView.as_view()),

    path("forgot-password/", ForgotPasswordView.as_view()),

    path("reset-password/<uidb64>/<token>/", ResetPasswordView.as_view()),

]