from functools import wraps

from django.contrib.sessions.models import Session
from django.http import HttpRequest

from users.services.db import get_anonymous_user_by_session, add_anonymous_user


def check_for_user_cookie(func):
    """
    This decorator check if a user with cookie 'session_key' exists.
    If not then create new user in db, and return it.
    """

    @wraps(func)
    def wrapper(self, request: HttpRequest, *args, **kwargs):
        # TODO: можно без обращения к дб, но сессии лежат в кэше так что норм
        session_key = request.session.session_key
        try:
            assert session_key is not None
        except AssertionError:
            raise IncognitoBrowserUsage
        session = Session.objects.get(session_key=session_key)
        user = get_anonymous_user_by_session(session=session)

        if user is None:
            user = add_anonymous_user(session=session)

        return func(self, request, *args, user=user, **kwargs)

    return wrapper


def is_owner(func):
    """Check if the user is the owner of the instance."""

    @wraps(func)
    def wrapper():
        return func()

    return wrapper


class DecoratorException(Exception):
    """Exception in decorators module."""
    pass


class IncognitoBrowserUsage(DecoratorException):
    """User uses browser in incognito mode."""

    def __init__(self):
        self.message = 'You should off incognito mode to use this app.'
