import json


def get_quiz_data() -> dict:
    return json.loads(TEST_QUIZ_JSON)


TEST_QUIZ_JSON = """{
  "name": "Quiz 2",
  "description": "Descr of quiz 2",
  "questions": [
    {
      "text": "Question 1 ??",
      "question_type": "text",
      "answer_options": []
    },
    {
      "text": "Question 2 ??",
      "question_type": "choose_one",
      "answer_options": [
{"text": "answer option 1"},
{"text": "answer option 2"},
{"text": "answer option 3"}]
    },
    {
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
