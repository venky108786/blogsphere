from rest_framework import serializers
from .models import UserProfile, Follow
from django.contrib.auth.models import User

# ✅ User Serializer to return only basic user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

# ✅ User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer to show user details
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["user", "followers", "following"]

    def get_followers(self, obj):
        """Return the list of followers as usernames."""
        return [follower.user.username for follower in obj.followers.all()]

    def get_following(self, obj):
        """Return the list of users this user follows as usernames."""
        return [following.user.username for following in obj.following.all()]

# ✅ Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(source="follower.user.username", read_only=True)
    following = serializers.CharField(source="following.user.username", read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
