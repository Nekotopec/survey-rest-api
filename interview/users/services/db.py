from ..models import AnonymousUser
from django.core.exceptions import ValidationError
from django.contrib.sessions.models import Session


def add_anonymous_user(session: Session):
    """
    Add anonymous user to database and returns it.
    """
    user = AnonymousUser(session=session)
    user.save()
    return user


def get_anonymous_user_by_session(session):
    try:
        user = AnonymousUser.objects.get(session=session)
    except (ValidationError, AnonymousUser.DoesNotExist):
        return None
    return user
