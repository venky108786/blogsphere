from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST
from rest_framework import generics, permissions
from blog.models import Post, Notification
from .serializers import UserSerializer, FollowSerializer
from .models import Follow
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_invalid(self, form):
        #Add a message when login fails
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))
def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "users/register.html", {"error": "Passwords do not match!"})

        # Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=make_password(password)  # Hashing the password
        )
        return redirect("login")  # Redirect to login page after successful registration

    return render(request, "users/register.html")

class FollowCreateView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class FollowUnfollowView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Follow.objects.get(follower=self.request.user, following_id=self.kwargs['user_id'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user)  # ✅ Only show user's posts
        return context


# User = get_user_model()
#
# class UserProfileView(View):
#     def get(self, request, username):
#         user = get_object_or_404(User, username=username)
#         return render(request, "users/profile.html", {"profile_user": user})

User = get_user_model()

class UserSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if query:
            users = User.objects.filter(username__icontains=query).values('id', 'username')
            return JsonResponse(list(users), safe=False)
        return JsonResponse([], safe=False)


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from .models import UserProfile
# from blogs.models import Post

User = get_user_model()

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    followers = user_profile.followers.all()
    following = user_profile.following.all()
    user_posts = Post.objects.filter(author=user).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated:
        current_profile = request.user.userprofile
        is_following = user_profile.followers.filter(id=current_profile.id).exists()

    context = {
        'user_profile': user_profile,
        'user': user,
        'followers': followers,
        'following': following,
        'user_posts': user_posts,
        'is_following': is_following,  # 👈 Send to template
    }
    return render(request, 'users/profile.html', context)


@require_POST
@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = get_object_or_404(UserProfile, user=target_user)
    current_profile = request.user.user_profile

    # Prevent self-following
    if target_profile != current_profile:
        current_profile.follow(target_profile)

        # Create a notification
        Notification.objects.create(
            sender=request.user,
            receiver=target_user,
            message=f"{request.user.username} followed you.",
            notification_type='follow'
        )

    return redirect('user_profile', username=username)

@require_POST
@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = get_object_or_404(UserProfile, user=target_user)
    current_profile = request.user.user_profile

    if target_profile != current_profile:
        current_profile.unfollow(target_profile)

    return redirect('user_profile', username=username)


User = get_user_model()

@require_POST
@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = get_object_or_404(UserProfile, user=target_user)
    current_user_profile = request.user.userprofile  # 👈 Get logged-in user's profile

    if target_profile.followers.filter(id=current_user_profile.id).exists():
        # 🔻 Already following → UNFOLLOW
        target_profile.followers.remove(current_user_profile)

        # ❗ Add notification for unfollow
        Notification.objects.create(
            sender=request.user,
            receiver=target_user,
            message=f"{request.user.username} unfollowed you.",
            notification_type='unfollow'
        )
    else:
        #Not following → FOLLOW
        target_profile.followers.add(current_user_profile)

        #Follow notification
        Notification.objects.create(
            sender=request.user,
            receiver=target_user,
            message=f"{request.user.username} followed you.",
            notification_type='follow'
        )

    return redirect("user_profile", username=target_user.username)
