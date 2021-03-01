from django.urls import path, include
from quiz.views.views import (QuizListView, QuizView)
from quiz.views.api_views import AnswerResponsesList, QuizViewSet, \
    AnswerResponsesViewSet
from rest_framework.routers import SimpleRouter
# from rest_framework_swagger.views import get_swagger_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

router = SimpleRouter()

router.register('quizzes', QuizViewSet)
router.register('answer_responses', AnswerResponsesViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Quizzes api",
        default_version='v1',
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
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
