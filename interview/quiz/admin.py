from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import AnswerOption, Question, Quiz, AnswerToQuestion, \
    AnswerResponse


# Register your models here.
class AnswerOptionAdmin(NestedModelAdmin):
    list_display = (
        'text',
    )


class AnswerOptionInline(NestedStackedInline):
    list_display = (
        'text',
    )
    model = AnswerOption
    extra = 0


class QuestionAdmin(NestedModelAdmin):
    list_display = (
        'text',
        'question_type',
    )


class QuestionInline(NestedStackedInline):
    list_display = (
        'text',
        'question_type',
    )
    model = Question
    inlines = [AnswerOptionInline]
    extra = 1


class QuizAdmin(NestedModelAdmin):
    list_display = (
        'name',
        'start_date',
        'description',
    )
    inlines = [QuestionInline]


class AnswerToQuestionInline(NestedStackedInline):
    model = AnswerToQuestion


class AnswerResponseAdmin(NestedModelAdmin):
    model = AnswerResponse
    inlines = [AnswerToQuestionInline]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(AnswerResponse, AnswerResponseAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(AnswerOption, AnswerOptionAdmin)
