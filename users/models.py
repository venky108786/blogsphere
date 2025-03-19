from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following", blank=True)

    def follow(self, profile):
        """Follow a user."""
        self.following.add(profile)

    def unfollow(self, profile):
        """Unfollow a user."""
        self.following.remove(profile)

    def is_following(self, profile):
        """Check if following a user."""
        return self.following.filter(id=profile.id).exists()

    def __str__(self):
        return self.user.username

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name="following_rel", on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name="followers_rel", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"
