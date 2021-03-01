from django.http import HttpResponse, HttpRequest
from django.views import View

from django.contrib.sessions.models import Session
from users.services.db import get_anonymous_user_by_session, add_anonymous_user


class BaseView(View):

    def dispatch(self, request, *args, **kwargs):
        user = self._get_anon_user(request)
        kwargs['user'] = user
        return super(BaseView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def _get_anon_user(request: HttpRequest):
        """
        Get user by `session_id`.
        If there is no user in table with this `session_id`
        creates and returns it.
        """

        session_key = request.session.session_key

        if not session_key:
            request.session.save()
        session_key = request.session.session_key

        session = Session.objects.get(session_key=session_key)
        user = get_anonymous_user_by_session(session=session)

        if user is None:
            user = add_anonymous_user(session=session)

        return user
