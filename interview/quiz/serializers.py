from rest_framework import serializers
from .models import AnswerToQuestion, Question, AnswerResponse, Quiz, \
    AnswerOption
from .validators import validate_answer_response


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True,
                                            source='answeroption_set',
                                            required=False)
    pk = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = ['pk', 'text', 'question_type', 'answer_options']

    def create(self, validated_data):
        answer_options = validated_data.pop('answeroption_set')

        if validated_data['question_type'] == 'text':
            return Question.objects.create(**validated_data)

        question = Question.objects.create(**validated_data)
        for answer_option in answer_options:
            answer_option['question'] = question
            AnswerOptionSerializer().create(answer_option)

        return question


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['name', 'description', 'id']


class QuizDetailSerializer(QuizSerializer):
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Quiz
        fields = ['name', 'description', 'absolute_url', 'questions']

    def create(self, validated_data: dict):
        questions: list = validated_data.pop('question_set')
        quiz_data = validated_data
        quiz = Quiz.objects.create(**quiz_data)

        for question in questions:
            question['quiz'] = quiz
            QuestionSerializer().create(question)

        return quiz


class AnswerToQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerToQuestion
        fields = ['question', 'question', 'text', 'answer_options']


class AnswerResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerResponse
        fields = ['id', 'user', 'quiz']


class AnswerResponseDetailSerializer(serializers.ModelSerializer):
    answers_to_questions = (
        AnswerToQuestionSerializer(many=True, source='answertoquestion_set')
    )

    class Meta:
        model = AnswerResponse
        fields = ['user', 'quiz', 'answers_to_questions']

    def validate(self, attrs):
        validated_data = super(AnswerResponseSerializer, self).validate(attrs)
        validate_answer_response(attrs)
        return validated_data

    def create(self, validated_data: dict):
        answers_to_questions = validated_data.pop('answertoquestion_set')
        answer_response = super().create(validated_data)
        for answer in answers_to_questions:
            answer['answer_response'] = answer_response
            AnswerToQuestionSerializer().create(answer)

        return answer_response
