from django.http.request import QueryDict
from .db import add_answer_response, add_answer_to_question


def save_quiz_data(user, raw_data: type(QueryDict)):
    """
    Save post data from Quiz.post view.
    """
    answer_response = add_answer_response(user)
    questions = list(raw_data.lists())

    for question in questions[1:]:
        add_answer_to_question(question[0], question[1])

    return
