from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import UserProfile, Post, Comment, Like, Follow, Notification
from .permissions import IsAdminOrAuthor
from .serializers import (
    UserProfileSerializer, PostSerializer, CommentSerializer,
    LikeSerializer, FollowSerializer, NotificationSerializer
)

# 🔹 User Profile View
class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the logged-in user's profile"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile  # Get the logged-in user's profile


# 🔹 Post Views
class PostListCreateView(generics.ListCreateAPIView):
    """List all posts and allow authenticated users to create a post"""
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Auto-assign logged-in user


class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """Ensure only the owner can update"""
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You are not the owner of this post!")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the owner can delete"""
        if instance.user != self.request.user:
            raise PermissionDenied("You cannot delete this post!")
        instance.delete()


# 🔹 Comment Views
class CommentListCreateView(generics.ListCreateAPIView):
    """List comments and allow users to create a comment"""
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign user automatically


# 🔹 Like Views (Preventing Duplicate Likes)
class LikeCreateView(generics.CreateAPIView):
    """Allow users to like a post (only once per post)"""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.validated_data['post']
        existing_like = Like.objects.filter(user=self.request.user, post=post).first()
        if existing_like:
            raise PermissionDenied("You have already liked this post!")
        serializer.save(user=self.request.user)


# 🔹 Follow Views (Preventing Duplicate Follow)
class FollowCreateView(generics.CreateAPIView):
    """Allow users to follow other users (but prevent duplicate follows)"""
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        followed_user = serializer.validated_data['following']
        if Follow.objects.filter(follower=self.request.user, following=followed_user).exists():
            raise PermissionDenied("You are already following this user!")
        serializer.save(follower=self.request.user)


# 🔹 Notification Views
class NotificationListView(generics.ListAPIView):
    """List notifications for the logged-in user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Only authors or admins can delete posts."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrAuthor]