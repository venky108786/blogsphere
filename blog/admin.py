from django.contrib import admin
from .models import UserProfile, Post, Comment, Like, Follow, Notification

# Registering all models to manage them in the Django admin panel
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Notification)
