from ..models import (Quiz, Question, AnswerOption, AnswerResponse,
                      AnswerToQuestion)
from django.core.exceptions import ValidationError
import uuid


def get_quiz(id):
    """
    Returns Quiz object by id.
    If there is no quiz in db with this if returns None.
    """

    try:
        return Quiz.objects.get(id=id)
    except (ValidationError, Quiz.DoesNotExist):
        return None


def get_questions_of_quiz(quiz: Quiz):
    questions = Question.objects.filter(quiz__id=quiz.id)
    return questions


def get_answer_options_of_question(question: Question):
    """
    Returns list of instances of `AnswerOption`.
    If there is no `answer_option` in database for current question
    returns None.
    """
    try:
        return AnswerOption.objects.filter(question_id=question.id)
    except (ValidationError, AnswerOption.DoesNotExist):
        return None


def add_answer_response(user):
    """
    Add `AnswerResponse` to database.
    """
    answer_response = AnswerResponse(user=user)
    answer_response.save()
    return answer_response


def add_answer_to_question(question_id: str, answer_response: AnswerResponse,
                           answer: list):
    """
    Add `AnswerToQuestion` to database.
    """
    try:
        question = Question.objects.get(question_id=question_id)
    except Question.DoesNotExist:
        # TODO: реализовать кастомные ошибки
        raise KeyError
    kwargs = {
        'question': question,
        'answer_response': answer_response
    }

    # TODO: здесь можно реализовать цепочку обязанностей для расширения,
    #  но тогда необходимо пересматривать модели и формы
    if question.question_type == question.TEXT:
        answer_to_question = AnswerToQuestion(text=answer[0],
                                              **kwargs)
    else:
        answer_to_question = AnswerToQuestion(**kwargs)
        for ans in answer:
            # TODO: остановился здесь
            answer_to_question.answer_options.add()


def get_answer_responses_by_user_id(user_id):
    return AnswerResponse.objects.filter(user_id=user_id)
