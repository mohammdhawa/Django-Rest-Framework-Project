from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)


# Define a custom permission class to handle review-specific permissions
class ReviewUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - Read-only access (GET, HEAD, OPTIONS) to any user.
    - Write access (POST, PUT, DELETE) only to the user who created the review.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determines if the requesting user has permission to perform the action.

        Args:
            request: The current HTTP request instance.
            view: The view instance handling the request.
            obj: The specific object being accessed (in this case, a review object).

        Returns:
            bool: True if the user is allowed to perform the action, False otherwise.
        """

        # SAFE_METHODS include HTTP methods like GET, HEAD, and OPTIONS,
        # which are read-only and do not modify the data.
        if request.method in permissions.SAFE_METHODS:
            # Allow read-only access to all users.
            return True
        else:
            # For non-safe methods (e.g., POST, PUT, DELETE),
            # grant permission only if the requesting user is the owner of the review.
            return obj.review_user == request.user