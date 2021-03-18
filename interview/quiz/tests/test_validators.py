from abc import ABC, abstractmethod

import pytest
from rest_framework.serializers import ValidationError

from quiz import models
from quiz.tests import quizzes_data
from quiz.validators import (
    Validator,
    AnswerOptionsValidator,
    AttachmentToQuizValidator,
    QuestionTypesValidator
)


class NoValidatorException(Exception):
    """There is no validator in TestValidator class."""
    pass


class BuildDataCore:
    """Mixin to building data for validators."""

    def build_data(self, data, quiz):
        data['quiz'] = quiz
        answers_set = self._build_answers_set(data)
        data['answertoquestion_set'] = answers_set

        return data

    def _build_answers_set(self, data):
        answers = data.pop('answers_to_questions')
        answers_set = list()
        for answer in answers:
            answer['question'] = models.Question.objects.get(
                pk=int(answer['question']))
            answer['answer_options'] = self._build_answer_options(answer)
            answers_set.append(answer)
        return answers_set

    def _build_answer_options(self, answer):
        answer_options = list()
        for option in answer['answer_options']:
            answer_options.append(models.AnswerOption.objects.get(id=option))
        return answer_options


class AbstractTestAnswerResponseValidator(ABC, BuildDataCore):
    """Abstract class for making tests for validators."""

    # Validator for testing.
    validator: type(Validator) = None

    def test_validator_existence(self):
        if self.validator is None:
            raise NoValidatorException(
                f'There is no validator class in {self.__class__}')

    def test_good_data(self, create_quiz):
        """Test good data validation."""
        good_data = quizzes_data.get_test_answer_response_data()
        data = self.build_data(good_data, create_quiz)
        self.validator().validate(data)

    def test_bad_data(self, create_quiz):
        """Test bad data validation."""

        good_data = quizzes_data.get_test_answer_response_data()
        bad_data = self.make_bad_data(good_data)
        self.check_bad_data(bad_data, create_quiz)

    @abstractmethod
    def make_bad_data(self, data):
        """Make bad data for testing bad data validation."""
        pass

    def check_bad_data(self, bad_data, quiz):
        data = self.build_data(bad_data, quiz)
        with pytest.raises(ValidationError) as ex:
            self.validator().validate(data)


class TestAnswerOptionValidator(AbstractTestAnswerResponseValidator):
    validator = AnswerOptionsValidator

    def make_bad_data(self, data):
        """Add bad answer option to `answer_to_question`."""
        data['answers_to_questions'][1]['answer_options'].append(4)
        return data


class TestAttachmentToQuizValidator(AbstractTestAnswerResponseValidator):
    validator = AttachmentToQuizValidator

    def test_bad_data(self, create_quiz, create_question):
        question_id = create_question
        good_data = quizzes_data.get_test_answer_response_data()
        bad_data = self.make_bad_data(good_data, question_id)
        self.check_bad_data(bad_data, create_quiz)

    def make_bad_data(self, data, question_id):
        answer_to_bad_question = self._make_answer_to_bad_question(question_id)
        data['answers_to_questions'].append(answer_to_bad_question)
        return data

    def _make_answer_to_bad_question(self, question_id):
        answer_to_question = {'question': question_id, 'text': 'dsfsdfsdf',
                              'answer_options': []}
        return answer_to_question


class TestQuestionTypesValidator(AbstractTestAnswerResponseValidator):
    validator = QuestionTypesValidator

    def make_bad_data(self, data):
        data['answers_to_questions'][0]['answer_options'].append(1)
        return data

    def test_one_choice_type(self, create_quiz):
        data = quizzes_data.get_test_answer_response_data()
        bad_data = self._make_bad_many_choices(data)
        self.check_bad_data(bad_data, create_quiz)

    def _make_bad_many_choices(self, data):
        data['answers_to_questions'][1]['answer_options'].append(2)
        return data
