from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

from quiz.views.api_views import QuizViewSet, \
    AnswerResponsesViewSet
from quiz.views.views import (QuizListView, QuizView)

router = SimpleRouter()

router.register('quizzes', QuizViewSet)
router.register('answer_responses', AnswerResponsesViewSet)
api_info = openapi.Info(
    title="Quizzes api",
    default_version='v1',
    description="Description",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('list/', QuizListView.as_view(), name='quiz-list'),
    path(r'quiz/<id>/', QuizView.as_view(), name="quiz-view"),
    # path('answers_responses/', AnswerResponsesList.as_view()),
    path(r'', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/', include(router.urls))
]
