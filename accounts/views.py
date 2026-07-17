from rest_framework import generics
from .models import CustomUser, Follow
from .serializers import RegisterSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, ProfileSerializer, FollowSerializer, PublicProfileSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()



class RegisterView(APIView):
    permission_classes = [AllowAny]   # ✅ MUST BE THIS

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ProfileSerializer(request.user)

        return Response(serializer.data)
    

    def patch(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)
    




class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            user = CustomUser.objects.get(id=pk)

        except CustomUser.DoesNotExist:

            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserProfileSerializer(user)

        return Response(serializer.data)
    
class PublicProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        user = get_object_or_404(
            CustomUser,
            username=username
        )

        serializer = PublicProfileSerializer(user)

        return Response(serializer.data)
    
class FollowUserView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, username):

        user_to_follow = get_object_or_404(
            CustomUser,
            username=username
        )

        if request.user == user_to_follow:

            return Response({
                "error": "You cannot follow yourself"
            })

        already_following = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        ).exists()

        if already_following:

            return Response({
                "message": "Already following"
            })

        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

        return Response({
            "message": f"You followed {username}"
        })

class UnfollowUserView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, username):

        user_to_unfollow = get_object_or_404(
            CustomUser,
            username=username
        )

        Follow.objects.filter(
            follower=request.user,
            following=user_to_unfollow
        ).delete()

        return Response({
            "message": f"You unfollowed {username}"
        })
    

class FollowersListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        user = get_object_or_404(
            CustomUser,
            username=username
        )

        followers = Follow.objects.filter(
            following=user
        )

        data = [
            follow.follower.username
            for follow in followers
        ]

        return Response(data)
    


class FollowingListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):

        user = get_object_or_404(
            CustomUser,
            username=username
        )

        following = Follow.objects.filter(
            follower=user
        )

        data = [
            follow.following.username
            for follow in following
        ]

        return Response(data)
    

from django.conf import settings

class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        print("🔥 FORGOT PASSWORD HIT")

        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = (
            f"http://localhost:5173/reset-password/{uid}/{token}"
        )

        print("📧 Sending email to:", email)
        print("🔗 Reset Link:", reset_link)

        try:
            send_mail(
                "Reset Password - Musify",
                f"Click here to reset password:\n\n{reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            print("✅ EMAIL SENT")

        except Exception as e:
            print("❌ EMAIL ERROR:", str(e))

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        print("🔗 Reset Link:", reset_link)

        return Response({
            "message": "Reset link generated",
            "reset_link": reset_link
        })
    


class ResetPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        password = request.data.get("password")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except:
            return Response({"error": "Invalid link"})

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"})

        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful"})