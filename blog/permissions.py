from rest_framework import permissions

class IsAdminOrAuthor(permissions.BasePermission):
    """Custom permission to allow only admins or post authors to delete."""

    def has_object_permission(self, request, view, obj):
        # Admins can delete any post
        if request.user.is_staff:
            return True
        # Post authors can delete their own posts
        return obj.author == request.user
