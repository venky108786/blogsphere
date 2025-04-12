from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        null=False,
        blank=False
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who commented
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Comment belongs to a post
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who liked
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Liked post
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"



class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('unfollow', 'Unfollow'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications", null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='like')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.notification_type}"
