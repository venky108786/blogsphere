from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .views import UserRegisterView, FollowCreateView, FollowUnfollowView, \
    CustomLoginView, RegisterView, UserSearchView, follow_user, unfollow_user

urlpatterns = [
    path('register/', RegisterView, name='register'),  # Use the HTML form view
    path('api/register/', UserRegisterView.as_view(), name='api-register'),# DRF API for registration
    path('follow/', FollowCreateView.as_view(), name='follow-create'),
    path('unfollow/<int:user_id>/', FollowUnfollowView.as_view(), name='unfollow'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('profile/<str:username>/', views.profile_view, name='user_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow-user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow-user'),
    path('follow/<str:username>/', follow_user, name='follow-user'),
    path('unfollow/<str:username>/', unfollow_user, name='unfollow-user'),
    path('toggle-follow/<str:username>/', views.toggle_follow, name='toggle_follow'),

    # Authentication Routes
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
