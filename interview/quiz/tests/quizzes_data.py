import json


def get_test_quiz_data() -> dict:
    return json.loads(TEST_QUIZ_JSON)


def get_test_answer_response_data() -> dict:
    return json.loads(GOOD_ANSWER_RESPONSE_DATA)


TEST_QUIZ_JSON = """{
  "name": "Quiz 2",
  "description": "Descr of quiz 2",
  "questions": [
    {
      "pk": "1",
      "text": "Question 1 ??",
      "question_type": "text",
      "answer_options": []
    },
    {
      "pk": "2",
      "text": "Question 2 ??",
      "question_type": "choose_one",
      "answer_options": [
{"text": "answer option 1"},
{"text": "answer option 2"},
{"text": "answer option 3"}]
    },
    { "pk": "3",
      "text": "Question 3 ??",
      "question_type": "choose_many",
      "answer_options": [
{"text": "answer option 1"},
{"text": "answer option 2"},
{"text": "answer option 3"}]
    }
  ]
}
"""

GOOD_ANSWER_RESPONSE_DATA = """{
        "answers_to_questions": [
            {
                "question": 1,
                "text": "dsfsdfsdf",
                "answer_options": []
            },
            {
                "question": 2,
                "text": "",
                "answer_options": [
                    1
                ]
            },
            {
                "question": 3,
                "text": "",
                "answer_options": [
                    5,
                    6
                ]
            }
        ]
    }
"""
