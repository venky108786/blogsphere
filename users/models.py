from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        self.following.add(profile)
        profile.followers.add(self)

    def unfollow(self, profile):
        self.following.remove(profile)
        profile.followers.remove(self)


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name="following_rel", on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name="followers_rel", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"