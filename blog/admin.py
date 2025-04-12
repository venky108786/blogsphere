from django.contrib import admin
from .models import Post, Comment, Like, Notification

# Registering all models to manage them in the Django admin panel
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Notification)
