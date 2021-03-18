import pytest

from quiz import serializers
from quiz.models import Quiz, AnswerResponse
from quiz.tests.quizzes_data import (
    get_test_quiz_data,
    get_test_answer_response_data
)
from users.models import AnonymousUser


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


def make_quiz():
    """Make new quiz with `quiz_data`."""
    quiz_data = get_test_quiz_data()
    quiz_s = serializers.QuizDetailSerializer(data=quiz_data)
    quiz_s.is_valid()
    quiz = quiz_s.create(quiz_s.validated_data)
    return quiz


def make_answer_response(user_id: int, quiz: Quiz) -> AnswerResponse:
    answer_response_data = get_test_answer_response_data()
    answer_response_data['quiz'] = quiz.id
    answer_response_data['user'] = user_id
    answer_response_serializer = serializers.AnswerResponseDetailSerializer(
        data=answer_response_data
    )
    answer_response_serializer.is_valid()
    answer_response = answer_response_serializer.create(
        answer_response_serializer.validated_data
    )
    return answer_response


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


@pytest.fixture(scope='function')
def create_user(db, client) -> AnonymousUser:
    client.get('/api/quizzes/')
    user = AnonymousUser.objects.all()[0]
    yield user
    user.delete()


@pytest.fixture(scope='function')
def create_user_answer_response(create_user, client, db, create_quiz):
    user = create_user
    quiz = create_quiz
    answer_response = make_answer_response(user.id, quiz)
    yield answer_response
    answer_response.delete()
