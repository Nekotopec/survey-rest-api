import uuid

from django.db import models

from interview.settings import BASE_URL
from users.models import AnonymousUser


# Create your models here.


class Quiz(models.Model):
    """Model of quiz."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.fields.CharField(max_length=255)
    start_date = models.fields.DateTimeField(auto_now_add=True)
    description = models.fields.TextField()

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.name

    def absolute_url(self):
        return "{}/quizzes/{}/".format(
            BASE_URL, self.id
        )


class Question(models.Model):
    """ Model of question."""

    # Questions types
    TEXT = 'text'
    CHOOSE_ONE = 'choose_one'
    CHOOSE_MANY = 'choose_many'

    text = models.fields.TextField()
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    question_type = models.fields.CharField(
        max_length=30,
        choices=[
            (TEXT, 'Question with text answer.'),
            (CHOOSE_ONE, 'Question with one choice.'),
            (CHOOSE_MANY, 'Question with many choices.')
        ],
        default=TEXT
    )

    def __str__(self):
        return self.text

    def get_answers(self):
        return AnswerOption.objects.filter(question_id=self.id)


class AnswerOption(models.Model):
    text = models.fields.CharField(max_length=255)
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text


class AnswerToQuestion(models.Model):
    """ Model for answer to the question."""

    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    text = models.TextField(null=True, blank=True)
    answer_options = models.ManyToManyField('AnswerOption', blank=True)
    answer_response = models.ForeignKey('AnswerResponse',
                                        on_delete=models.CASCADE)


class AnswerResponse(models.Model):
    """ Answer to full quiz from the user."""
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    user = models.ForeignKey('users.AnonymousUser',
                             on_delete=models.DO_NOTHING)
