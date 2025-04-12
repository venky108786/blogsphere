from django.urls import path
from .views import (
    PostListCreateView, PostRetrieveUpdateDeleteView,
    CommentListCreateView, CommentRetrieveUpdateDeleteView,
    LikeCreateView, UnlikeDeleteView, PostCreateView, NotificationListView,
    CommentCreateWithNotificationView, PostDetailView
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteView.as_view(), name='post-detail'),
    path('post/view/<int:pk>/', PostDetailView.as_view(), name='post-detail-page'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDeleteView.as_view(), name='comment-detail'),
    path('comments/post/<int:post_id>/', CommentCreateWithNotificationView.as_view(), name='comment-post'),
    path('like/', LikeCreateView.as_view(), name='like-create'),
    path('unlike/<int:post_id>/', UnlikeDeleteView.as_view(), name='unlike'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]
