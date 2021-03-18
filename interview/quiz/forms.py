from django import forms
from django.forms import models

from .models import Quiz, Question
from .services.db import get_questions_of_quiz, get_answer_options_of_question


class QuizForm(models.ModelForm):
    class Meta:
        model = Quiz
        fields = ()

    def __init__(self, *args, **kwargs):
        self.quiz = kwargs.pop('quiz')
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.questions = self._get_questions_of_quiz()
        self.questions_forms = self._build_question_forms()

    def _get_questions_of_quiz(self):
        return get_questions_of_quiz(self.quiz)

    def _build_question_forms(self):
        """
        Build list of question forms `QuestionForm`
        """
        question_forms = list()
        for question in self.questions:
            question_form = QuestionForm(question=question)
            question_forms.append(question_form)

        return question_forms


class QuestionForm(forms.forms.Form):
    FIELDS = {
        Question.TEXT: forms.CharField,
        Question.CHOOSE_ONE: forms.ChoiceField,
        Question.CHOOSE_MANY: forms.MultipleChoiceField
    }

    WIDGETS = {
        Question.TEXT: forms.Textarea,
        Question.CHOOSE_ONE: forms.RadioSelect,
        Question.CHOOSE_MANY: forms.CheckboxSelectMultiple
    }

    def __init__(self, *args, **kwargs):
        self.question: Question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields = self._get_fields()

    def get_widget(self, **kwargs):
        """
        Returns widget by `question_type`.
        """
        attrs = kwargs

        try:
            return self.WIDGETS[self.question.question_type](attrs=attrs)
        except KeyError:
            return self.WIDGETS[self.question.TEXT]

    def _get_field(self, **kwargs):
        try:
            return self.FIELDS[self.question.question_type](**kwargs)
        except KeyError:
            return self.FIELDS[self.question.TEXT]

    def get_answer_options(self):
        """
        Returns list of answer options for `question`.
        """

    def _get_formatted_choices(self, answer_options):
        choices = list()
        for answer_option in answer_options:
            choices.append((answer_option.pk, answer_option.text))
        return choices

    def _get_name_attr(self):
        return str(self.question.id)

    def _get_fields(self) -> dict:
        kwargs = dict()
        widget_attrs = {'name': self._get_name_attr()}

        if (self.question.question_type == self.question.CHOOSE_ONE or
                self.question.question_type == self.question.CHOOSE_MANY):
            answer_options = get_answer_options_of_question(self.question)
            kwargs['choices'] = self._get_formatted_choices(answer_options)

            # Need for delete markers from form.
            # TODO: переделать захаркоженную вещь
            widget_attrs['class'] = 'custom-radio-list'
            if self.question.question_type == self.question.CHOOSE_ONE:
                kwargs['help_text'] = 'Choose one option.'
            else:
                kwargs['help_text'] = 'Choose several options.'

        elif self.question.question_type == self.question.TEXT:
            widget_attrs['style'] = "width:100%;"

        kwargs['label'] = self.question.text

        kwargs['widget'] = self.get_widget(**widget_attrs)
        field = self._get_field(**kwargs)

        return {f'{self.question.pk}': field}
