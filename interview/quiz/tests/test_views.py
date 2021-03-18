import json

from django.test.client import Client

from quiz import models as quiz_models
from quiz.tests.quizzes_data import (
    get_test_answer_response_data,
    get_test_quiz_data
)
from users import models as user_models


class TestAnswerResponseViewSet:

    def test_get_answers_by_id(
            self,
            client: Client,
            create_user: user_models.AnonymousUser,
            create_user_answer_response: quiz_models.AnswerResponse,
            create_quiz: quiz_models.Quiz):
        """
        Check list of answers of current user.
        """

        quiz_id = create_quiz.id
        user_id = create_user.id
        answer_response_id = create_user_answer_response.id
        response = client.get(f'/api/answer_responses/?user_id={user_id}')
        data = response.json()
        expected = [
            {
                'id': answer_response_id,
                'user': user_id,
                'quiz': str(quiz_id)
            }
        ]
        assert data == expected

    def test_receive_answer_response(
            self,
            client: Client,
            create_user: user_models.AnonymousUser,
            create_user_answer_response: quiz_models.AnswerResponse,
            create_quiz: quiz_models.Quiz):
        """
        Check answer response with current id.
        """

        quiz_id = create_quiz.id
        user_id = create_user.id
        answer_response_id = create_user_answer_response.id
        response = client.get(f'/api/answer_responses/{answer_response_id}/')
        data = response.json()
        expected = {'user': user_id, 'quiz': str(quiz_id),
                    'answers_to_questions': [
                        {'question': 1, 'text': 'dsfsdfsdf',
                         'answer_options': []},
                        {'question': 2, 'text': '', 'answer_options': [1]},
                        {'question': 3, 'text': '', 'answer_options': [5, 6]}]}

        assert data == expected

    def test_post_answer_response(
            self,
            client: Client,
            create_quiz: quiz_models.Quiz,
            create_user: user_models.AnonymousUser):
        """
        Test answer response posting.
        """

        quiz_id = create_quiz.id
        user_id = create_user.id
        data = get_test_answer_response_data()
        data['user'] = user_id
        data['quiz'] = str(quiz_id)
        client.post(
            path=f'/api/answer_responses/',
            data=json.dumps(data),
            content_type='application/json'
        )
        answer_response = quiz_models.AnswerResponse.objects.filter(
            quiz__id=quiz_id,
            user__id=user_id,
        )[0]

        assert (answer_response.quiz_id == quiz_id and
                answer_response.user_id == user_id and
                len(answer_response.answertoquestion_set.all()) == 3)

    def test_good_destroying(
            self,
            client: Client,
            create_quiz: quiz_models.Quiz,
            create_user: user_models.AnonymousUser,
            create_user_answer_response: quiz_models.AnswerResponse):
        """
        Test `answer_response` object destroying by the owner.
        """

        response = self._delete_answer_response(client,
                                                create_user_answer_response)
        assert response.status_code == 204
        assert len(quiz_models.AnswerResponse.objects.all()) == 0

    def test_bad_destroying(
            self,
            create_quiz: quiz_models.Quiz,
            create_user_answer_response: quiz_models.AnswerResponse
    ):
        """
        Test `answer_response` object destroying by a non-owner.
        """

        new_client = Client()
        response = self._delete_answer_response(new_client,
                                                create_user_answer_response)
        assert response.status_code == 401
        assert len(quiz_models.AnswerResponse.objects.all()) == 1

    @staticmethod
    def _delete_answer_response(
            client: Client,
            answer_response: quiz_models.AnswerResponse):
        """
        Delete answer response throw client session.
        """

        answer_response_id = answer_response.id
        url = f'/api/answer_responses/{answer_response_id}/'
        response = client.delete(path=url)
        return response

    def test_good_patch(
            self,
            client: Client,
            create_quiz: quiz_models.Quiz,
            create_user: user_models.AnonymousUser,
            create_user_answer_response: quiz_models.AnswerResponse
    ):
        """
        Test `answer_response` object patching by the owner.
        """

        response = self._patch_answer_response(client,
                                               create_user_answer_response)

        assert response.status_code == 200
        answer_instance = quiz_models.AnswerResponse.objects.all()[0]
        assert (answer_instance.answertoquestion_set.all()[0].text ==
                'new answer')
        assert (answer_instance.answertoquestion_set.all()[
                    1].answer_options.all()[0].id == 2)

    def test_bad_patch(
            self,
            client: Client,
            create_quiz: quiz_models.Quiz,
            create_user: user_models.AnonymousUser,
            create_user_answer_response: quiz_models.AnswerResponse
    ):
        """
        Test `answer_response` object patching by other user (non-owner).
        """

        new_client = Client()
        response = self._patch_answer_response(new_client,
                                               create_user_answer_response)
        assert response.status_code == 401

    @staticmethod
    def _patch_answer_response(
            client: Client,
            answer_response: quiz_models.AnswerResponse
    ):
        """
        Patch answer response throw client.
        """

        answer_response_id = answer_response.id
        quiz_id = answer_response.quiz_id
        url = f'/api/answer_responses/{answer_response_id}/'
        data = get_test_answer_response_data()
        data['quiz'] = str(quiz_id)
        data['answers_to_questions'][0] = {
            "question": 1,
            "text": "new answer",
            "answer_options": []
        }
        data['answers_to_questions'][1] = {
            "question": 2,
            "text": "",
            "answer_options": [2]
        }
        response = client.patch(path=url,
                                data=json.dumps(data),
                                content_type='application/json')
        return response


class TestQuizViewSet:
    url = '/api/quizzes/'

    def test_quizzes_list_getting(
            self,
            create_quiz,
            client,
    ):
        """
        Test getting `quiz` objects list.
        """

        response = client.get(path=self.url)
        assert response.status_code == 200

        quizzes_list = response.json()
        assert len(quizzes_list) == 1

        quiz_id = quizzes_list[0].get('id')
        assert quiz_id == str(create_quiz.id)

    def test_getting_quiz_by_id(
            self,
            create_quiz,
            client
    ):
        """
        Test `quiz` object getting by id.
        """

        response = client.get(f'{self.url}{str(create_quiz.id)}/')
        assert response.status_code == 200

        quiz_data = response.json()
        assert quiz_data.get('id') == str(create_quiz.id)

    def test_creating_quiz_object(
            self,
            admin_client
    ):
        """
        Test creating of `quiz` object.
        """

        response = self._create_quiz(admin_client)
        assert response.status_code == 201

        quiz = quiz_models.Quiz.objects.all()[0]
        assert quiz is not None
        assert len(quiz.question_set.all()) == 3

    def _create_quiz(self, client):
        """
        Make post request to quiz api.
        """
        data = get_test_quiz_data()
        response = client.post(self.url,
                               data=json.dumps(data),
                               content_type='application/json')
        return response

    def test_updating_quiz(
            self,
            create_quiz,
            admin_client
    ):
        """
        Test `quiz` object updating.
        """

        response = self._update_quiz(admin_client, create_quiz)
        assert response.status_code == 200

        quiz = quiz_models.Quiz.objects.all()[0]
        assert quiz.name == 'New quiz name.'

        question = quiz.question_set.all()[0]
        assert question.text == 'New question.'
        assert question.question_type == 'choose_one'
        assert len(question.answeroption_set.all()) == 3

    def test_quiz_creating_by_non_admin(
            self,
            client
    ):
        """
        Test creating of `quiz` object by non-admin user.
        """

        response = self._create_quiz(client)
        assert response.status_code == 401

    def test_quiz_updating_by_non_admin(
            self,
            client,
            create_quiz
    ):
        """
        Test updating of `quiz` object by non-admin user.
        """
        response = self._update_quiz(client, create_quiz)
        assert response.status_code == 401

    def _update_quiz(self, client, quiz):
        """Update quiz object by making patch request to api."""

        data = get_test_quiz_data()
        data['name'] = 'New quiz name.'
        question = data['questions'][0]
        question['text'] = 'New question.'
        question['question_type'] = 'choose_one'
        question['answer_options'] = [{"text": "answer option 1"},
                                      {"text": "answer option 2"},
                                      {"text": "answer option 3"}]
        data['questions'][0] = question

        response = client.patch(path=f'{self.url}{quiz.id}/',
                                data=json.dumps(data),
                                content_type='application/json')
        return response
