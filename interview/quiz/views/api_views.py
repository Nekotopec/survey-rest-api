from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from quiz.models import AnswerResponse, Quiz
from quiz.permissions import (
    OnlySafeMethodsOrAdmin,
    PatchOrDeleteIfOwnerOfAnswerOrAdmin
)
from quiz.serializers import (
    AnswerResponseSerializer, QuizDetailSerializer,
    QuizSerializer, AnswerResponseDetailSerializer
)
from quiz.services.db import get_answer_responses_by_user_id
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
        'default': QuizDetailSerializer,
        'list': QuizSerializer
    }


class AnswerResponsesViewSet(BaseView, MultiSerializerViewSet):
    serializers_classes = {'default': AnswerResponseDetailSerializer,
                           'list': AnswerResponseSerializer}
    queryset = AnswerResponse.objects.all()

    permission_classes = [PatchOrDeleteIfOwnerOfAnswerOrAdmin]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id is None:
            return super().get_queryset()

        else:
            return get_answer_responses_by_user_id(user_id)

    def create(self, request, *args, **kwargs):

        request.data['user'] = self.get_user_id(kwargs)
        return super().create(request, *args, **kwargs)

    @staticmethod
    def get_user_id(kwargs):
        return kwargs.get('user').id
