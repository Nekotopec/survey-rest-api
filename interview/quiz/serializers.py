from rest_framework import serializers

from .models import AnswerToQuestion, Question, AnswerResponse, Quiz, \
    AnswerOption
from .validators import validate_answer_response


class AnswerOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = AnswerOption
        fields = ['id', 'text']

    def create(self, validated_data):
        validated_data.pop('id', None)
        return super(AnswerOptionSerializer, self).create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True,
                                            source='answeroption_set',
                                            required=False)
    pk = serializers.IntegerField(required=False)

    class Meta:
        model = Question
        fields = ['pk', 'text', 'question_type', 'answer_options']

    def create(self, validated_data: dict):
        validated_data.pop('pk', None)
        answer_options = validated_data.pop('answeroption_set')

        if validated_data['question_type'] == 'text':
            return Question.objects.create(**validated_data)

        question = Question.objects.create(**validated_data)
        for answer_option in answer_options:
            answer_option['question'] = question
            AnswerOptionSerializer().create(answer_option)

        return question

    def update(self, instance, validated_data):
        answer_options = validated_data.pop('answeroption_set')
        question = super().update(instance, validated_data)
        answer_option_set = question.answeroption_set.all()
        if validated_data['question_type'] == 'text':
            return question

        for answer_option in answer_options:
            answer_option['question'] = question
            try:
                answer_option_instance = answer_option_set.get(
                    id=answer_option.get('id'))
                AnswerOptionSerializer().update(answer_option_instance,
                                                answer_option)
            except AnswerOption.DoesNotExist:
                AnswerOptionSerializer().create(answer_option)

        return question


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['name', 'description', 'id']


class QuizDetailSerializer(QuizSerializer):
    questions = QuestionSerializer(many=True, source='question_set')
    id = serializers.ReadOnlyField()

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'questions']

    def create(self, validated_data: dict):
        questions: list = validated_data.pop('question_set')
        quiz_data = validated_data
        quiz = Quiz.objects.create(**quiz_data)

        for question in questions:
            question['quiz'] = quiz
            QuestionSerializer().create(question)

        return quiz

    def update(self, instance, validated_data):

        questions: list = validated_data.pop('question_set')
        quiz = super().update(instance, validated_data)
        question_set = quiz.question_set.all()

        # Updating existing questions.
        for question in questions:
            question['quiz'] = quiz
            try:
                question_instance = question_set.get(pk=question.get('pk'))
                QuestionSerializer().update(question_instance, question)
            except Question.DoesNotExist:
                QuestionSerializer().create(question)
        return quiz

        # Create new questions
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
        validated_data = super().validate(attrs)
        validate_answer_response(attrs)
        return validated_data

    def create(self, validated_data: dict):
        answers_to_questions = validated_data.pop('answertoquestion_set')
        answer_response = super().create(validated_data)
        for answer in answers_to_questions:
            answer['answer_response'] = answer_response
            AnswerToQuestionSerializer().create(answer)

        return answer_response

    def update(self, instance: AnswerResponse, validated_data):
        answers_to_questions = validated_data.pop('answertoquestion_set')
        answer_response = super().update(instance, validated_data)
        for answer in answers_to_questions:
            answer['answer_response'] = answer_response
            answer_to_question_instance = instance.answertoquestion_set.get(
                answer_response=instance,
                question=answer.get('question')
            )
            AnswerToQuestionSerializer().update(answer_to_question_instance,
                                                answer)

        return answer_response
