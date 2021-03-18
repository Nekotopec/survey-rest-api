from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from quiz.forms import QuizForm
from quiz.models import Quiz
from quiz.services.db import get_quiz, get_questions_of_quiz
from quiz.views.base_views import BaseView


class QuizListView(BaseView, ListView):
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['host'] = self.request.get_host()
        return context


class QuizView(BaseView, View):
    """Class based view for quiz."""

    def get(self, request: HttpRequest, *args, **kwargs):
        user = kwargs.pop('user')
        quiz_id = kwargs.get('id')
        quiz = get_quiz(quiz_id)
        if not quiz:
            return HttpResponse(status=404)
        questions = get_questions_of_quiz(quiz)

        template_name = "quiz/quiz.html"
        # template_name = 'quiz/new_try.html'
        form = QuizForm(quiz=quiz, user=user)
        context = {
            'quiz': quiz,
            'questions': questions,
            'form': form,
            'user': user
        }

        # Set user cookie for anonymous user
        return render(request, template_name, context)
