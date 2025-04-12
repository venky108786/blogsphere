from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Notification

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested User Data

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at']

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        # Accept 'post' from context instead of request.data
        validated_data['post'] = self.context['post']
        return super().create(validated_data)
# Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'receiver', 'post', 'message', 'created_at', 'is_read']
