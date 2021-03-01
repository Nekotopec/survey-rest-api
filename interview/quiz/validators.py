from abc import abstractmethod, ABC
from rest_framework.exceptions import ValidationError
from quiz import models
from typing import List


# Chain of responsibilities validators

class AbstractValidator(ABC):

    @abstractmethod
    def __init__(self, validator=None):
        pass

    @abstractmethod
    def set_next(self, validator):
        pass

    @abstractmethod
    def validate(self, data) -> None:
        pass


class Validator(AbstractValidator):
    _next_validator: AbstractValidator = None

    def __init__(self, validator: AbstractValidator = None):
        super().__init__(validator)
        if validator:
            self.set_next(validator)

    def set_next(self, validator: AbstractValidator) -> AbstractValidator:
        self._next_validator = validator
        return validator

    @abstractmethod
    def validate(self, data) -> None:
        if self._next_validator:
            return self._next_validator.validate(data)

    @staticmethod
    def get_answers(data: dict):
        """Returns `answers_to_questions` data.
        Raise ValidationError if `answers_to_questions` is empty list."""
        answers = data.get('answertoquestion_set')
        if not answers:
            raise ValidationError(
                'There are no `answers_to_questions` in your post data'
            )
        return answers


class QuestionTypesValidator(Validator):

    def validate(self, data) -> None:
        answers = self.get_answers(data)
        for answer in answers:
            if self.check_text_question(answer):
                pass
            else:
                self.check_question_with_choices(answer)

        super().validate(data)

    @staticmethod
    def check_text_question(answer):
        if answer['question'].question_type == models.Question.TEXT:
            if not answer['text']:
                raise ValidationError(
                    'There is no answer.text for text type question. '
                    f'(question_id: {answer["question"].id})'
                )
            if answer['answer_options']:
                raise ValidationError(
                    'Answer options are allowed: question.type is `text` '
                    f'(question_id: {answer["question"].id})'
                )
            return True

    @staticmethod
    def check_question_with_choices(answer):
        if answer['text']:
            raise ValidationError(
                f'Text answer is not allowed:'
                f'question.type is `choose_one` or `choose_many` '
                f'(question_id: {answer["question"].id})'
            )
        if not answer['answer_options']:
            raise ValidationError(
                ('There is no answer option in answer for question with type '
                 '`choose_one` or `choose_many` '
                 f'(question_id: {answer["question"].id})')
            )
        if answer['question'].question_type == models.Question.CHOOSE_ONE:
            if len(answer['answer_options']) > 1:
                raise ValidationError(
                    'Too many answer options for `choose_one` question.type '
                    f'(question_id: {answer["question"].id})')
        return True


class AttachmentToQuizValidator(Validator):
    """
    Check for attachment to one quiz for every question and answer
    in `answer_response` data.
    """

    def validate(self, data) -> None:

        questions_id_set = self._get_questions_id_set_of_quiz(data.get('quiz'))
        received_questions_id_set = self._get_received_questions_id_set(data)
        try:
            assert questions_id_set == received_questions_id_set
        except AssertionError:
            raise ValidationError(
                'Bad question_ids for this quiz. '
                f'(questions: {received_questions_id_set - questions_id_set}'
            )
        super().validate(data)

    @staticmethod
    def _get_questions_id_set_of_quiz(quiz: models.Quiz) -> set:
        questions = quiz.question_set.all()
        question_id_set = set()
        for question in questions:
            question_id_set.add(question.pk)

        return question_id_set

    @staticmethod
    def _get_received_questions_id_set(data) -> set:
        questions_ids = set()
        answers = data.get('answertoquestion_set')

        for answer in answers:
            questions_ids.add(answer['question'].id)

        return questions_ids


class AnswerOptionsValidator(Validator):

    def validate(self, data) -> None:
        answer_options_dict = self._get_answer_options_dict(data)
        received_answers = self.get_answers(data)
        for answer in received_answers:
            received_options = self._get_received_options(answer)

            # Fot text questions.
            if not received_options:
                continue
            question_id = answer['question'].id
            self._check_question_options(answer_options_dict[question_id],
                                         received_options,
                                         question_id)

        super(AnswerOptionsValidator, self).validate(data)

    @staticmethod
    def _get_received_options(answer: dict):
        options = answer.get('answer_options')
        options_set = set([option.id for option in options])
        return options_set

    @staticmethod
    def _check_question_options(question_options: set,
                                received_options: set,
                                question_id):
        try:
            assert received_options == (received_options &
                                        question_options)
        except AssertionError:
            raise ValidationError(
                f'Bad answer options for question with '
                f'`question_id`={question_id}. '
                f'Available options are {question_options}'
            )

    def _get_answer_options_dict(self, data):
        quiz = data.get('quiz')
        answer_options = models.AnswerOption.objects.filter(question__quiz=quiz)
        answers = self.get_answers(data)
        answer_options_dict = dict()
        for answer in answers:
            question_id = answer['question'].id
            answer_options_dict[question_id] = set(answer_options.filter(
                question_id=question_id
            ).values_list('pk', flat=True))

        return answer_options_dict


chain: List[type(Validator)] = [
    AttachmentToQuizValidator,
    QuestionTypesValidator,
    AnswerOptionsValidator,
]


def validate_answer_response(data) -> None:
    res_validator = None
    for validator in chain[::-1]:
        res_validator = validator(res_validator)
    return res_validator.validate(data)
