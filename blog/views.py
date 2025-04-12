from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from rest_framework import generics, permissions, status
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment, Like, Notification
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, NotificationSerializer
from .permissions import IsAdminOrAuthor



class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrAuthor]

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure the logged-in user is set as the author
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)

        # 🔔 Notify post owner
        if comment.post.author != self.request.user:
            Notification.objects.create(
                receiver=comment.post.author,
                sender=self.request.user,
                post=comment.post,
                message=f"{self.request.user.username} commented on your post '{comment.post.title}'"
            )

class CommentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrAuthor]

class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        like = serializer.save(user=self.request.user)

        # 🔔 Create Notification for the post owner
        if like.post.author != self.request.user:
            Notification.objects.create(
                receiver=like.post.author,
                sender=self.request.user,
                post=like.post,
                message=f"{self.request.user.username} liked your post '{like.post.title}'"
            )


class UnlikeDeleteView(generics.DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Like.objects.get(user=self.request.user, post_id=self.kwargs['post_id'])


from django.shortcuts import render
from .models import Post

def home_view(request):
    all_posts = Post.objects.all().order_by('-created_at')
    liked_post_ids = []

    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'blog/home.html', {
        'all_posts': all_posts,
        'liked_post_ids': liked_post_ids,
    })

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by('-created_at')


class CommentCreateWithNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data, context={'request': request, 'post': post})
        if serializer.is_valid():
            comment = serializer.save(user=request.user)

            # 🔔 Create notification with actual comment text
            if post.author != request.user:
                Notification.objects.create(
                    sender=request.user,
                    receiver=post.author,
                    notification_type='comment',
                    post=post,
                    message=f'{request.user.username} commented on your post "{post.title}": {comment.content}'
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

