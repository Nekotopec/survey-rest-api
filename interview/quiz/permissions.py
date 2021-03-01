from rest_framework.permissions import SAFE_METHODS, IsAdminUser


class OnlySafeMethodsOrAdmin(IsAdminUser):
    """Allow any user use GET, HEAD, OPTIONS methods only."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(OnlySafeMethodsOrAdmin, self).has_permission(request, view)
