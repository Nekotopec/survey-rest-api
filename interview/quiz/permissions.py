from django.http import HttpRequest
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, BasePermission

from quiz.models import AnswerResponse


class OnlySafeMethodsOrAdmin(IsAdminUser):
    """Allow any user use GET, HEAD, OPTIONS methods only."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return super(OnlySafeMethodsOrAdmin, self).has_permission(request,
                                                                      view)


class PatchOrDeleteIfOwnerOfAnswerOrAdmin(BasePermission):

    def has_object_permission(self, request: HttpRequest, view,
                              obj: AnswerResponse):
        """
        Only an admin or the owner can Patch or delete
        the answer_response object.
        """
        # For admin users or safe methods.
        if (request.user and request.user.is_staff or
                request.method in SAFE_METHODS):
            return True

        if (obj.user.session and
                obj.user.session.session_key == request.session.session_key):
            return True
