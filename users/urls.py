from django.urls import path
from .views import FollowUnfollowView, FollowersListView, FollowingListView, UserProfileView

urlpatterns = [
    path('follow/<str:username>/', FollowUnfollowView.as_view(), name='follow-unfollow'),
    path('followers/<str:username>/', FollowersListView.as_view(), name='followers-list'),
    path('following/<str:username>/', FollowingListView.as_view(), name='following-list'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
]
