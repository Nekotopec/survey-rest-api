from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from quiz.models import AnswerResponse, Quiz
from quiz.services.db import get_answer_responses_by_user_id
from quiz.serializers import (AnswerResponseSerializer, QuizDetailSerializer,
                              QuizSerializer, AnswerResponseDetailSerializer)
from quiz.permissions import OnlySafeMethodsOrAdmin

from .base_views import BaseView


class AnswerResponsesList(BaseView, ListAPIView):
    queryset = AnswerResponse.objects.all()
    lookup_field = 'pk'
    serializer_class = AnswerResponseSerializer


class MultiSerializerViewSet(ModelViewSet):
    serializers_classes = None

    def get_serializer_class(self):
        try:
            return self.serializers_classes[self.action]
        except KeyError:
            return self.serializers_classes['default']


class QuizViewSet(BaseView, MultiSerializerViewSet):
    permission_classes = [OnlySafeMethodsOrAdmin]

    queryset = Quiz.objects.all()
    serializers_classes = {
        'update': QuizDetailSerializer,
        'create': QuizDetailSerializer,
        'retrieve': QuizDetailSerializer,
        'default': QuizSerializer,

    }


class AnswerResponsesViewSet(BaseView, MultiSerializerViewSet):
    serializers_classes = {'default': AnswerResponseDetailSerializer,
                           'list': AnswerResponseSerializer}
    queryset = AnswerResponse.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id is None:
            return super().get_queryset()
        else:
            return get_answer_responses_by_user_id(user_id)

    def create(self, request, *args, **kwargs):

        request.data['user'] = kwargs.get('user').id
        return super().create(request, *args, **kwargs)
