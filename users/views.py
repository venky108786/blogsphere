from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from blog.models import Notification
from .models import UserProfile
from .serializers import UserProfileSerializer, FollowSerializer

class FollowUnfollowView(APIView):
    """
    API to follow or unfollow a user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        user_to_follow = get_object_or_404(UserProfile, user__username=username)
        user_profile = request.user.user_profile  # Get the logged-in user's profile

        if user_profile.is_following(user_to_follow):
            user_profile.unfollow(user_to_follow)
            return Response({"message": f"Unfollowed {username}"}, status=status.HTTP_200_OK)
        else:
            user_profile.follow(user_to_follow)

            # ✅ Create a Notification
            Notification.objects.create(
                user=user_to_follow.user,  # The person being followed receives the notification
                message=f"{request.user.username} followed you"
            )

            return Response({"message": f"Followed {username}"}, status=status.HTTP_200_OK)
class FollowersListView(APIView):
    """
    API to get a list of followers of a user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(UserProfile, user__username=username)
        followers = user.followers.all()  # Get all users who follow this user
        serializer = UserProfileSerializer(followers, many=True)
        return Response({"followers": serializer.data})

class FollowingListView(APIView):
    """
    API to get a list of users this user follows.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(UserProfile, user__username=username)
        following = user.following.all()  # Get all users this user follows
        serializer = UserProfileSerializer(following, many=True)
        return Response({"following": serializer.data})

class UserProfileView(generics.RetrieveAPIView):
    """
    API to retrieve user profile details.
    """
    queryset = UserProfile.objects.all()  # ✅ Ensure it queries UserProfile
    serializer_class = UserProfileSerializer
    lookup_field = "user__username"  # ✅ Corrected field name
    lookup_url_kwarg = "username"
    permission_classes = [permissions.IsAuthenticated]

class FollowCreateView(generics.CreateAPIView):
    """
    API to create a follow relationship.
    """
    queryset = UserProfile.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
