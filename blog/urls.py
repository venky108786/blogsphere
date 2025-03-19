from django.urls import path
from .views import (
    PostListCreateView, PostRetrieveUpdateDeleteView,
    CommentListCreateView, LikeCreateView,
    NotificationListView
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]
