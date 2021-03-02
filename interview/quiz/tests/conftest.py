import os
import requests
import pytest
import json
from quiz.serializers import QuizDetailSerializer
from quiz.tests.quizzes_data import TEST_QUIZ_JSON, GOOD_ANSWER_RESPONSE_DATA
from users.models import AnonymousUser


def get_quiz_data() -> dict:
    return json.loads(TEST_QUIZ_JSON)


def get_answer_response_data():
    return json.loads(GOOD_ANSWER_RESPONSE_DATA)


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


def make_quiz():
    """Make new quiz with `quiz_data`."""
    quiz_data = get_quiz_data()
    quiz_s = QuizDetailSerializer(data=quiz_data)
    quiz_s.is_valid()
    quiz = quiz_s.create(quiz_s.validated_data)
    return quiz


@pytest.fixture(scope='function')
def create_quiz(db):
    """ Fixture for creating task."""
    quiz = make_quiz()
    yield quiz
    quiz.delete()


@pytest.fixture(scope='function')
def create_question(db) -> int:
    quiz = make_quiz()
    question_id = quiz.question_set.all()[0].id
    yield question_id
    quiz.delete()


# @pytest.fixture(scope='class')
# def create_user(django_db_blocker, client) -> int:
#     with django_db_blocker.unblock():
#         client.get('/api/quizzes/')
#         user = AnonymousUser.objects.all()[0]
#         yield user
#
#
# @pytest.fixture(scope='class')
# def create_user_answer_response(create_user, client):

#
# @pytest.fixture(scope='function')
# def create_user_answer_response():


@pytest.fixture(scope='function')
def patch_request(monkeypatch):
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code

        @staticmethod
        def iter_content(chunk_size):
            image_path = os.path.join(
                os.path.dirname(__file__),
                'static/kitty.jpg',
            )
            with open(image_path, 'rb') as f:
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    yield data

    def _wrap(status=200):

        def mock_get(*args, **kwargs):
            return MockResponse(status)

        monkeypatch.setattr(requests, 'get', mock_get)

    yield _wrap
