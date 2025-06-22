from rest_framework import serializers
from .models import Exam, Question, AnswerOption

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'question', 'answer_text', 'answer_image', 'is_correct']

    def validate(self, data):
        if not data.get('answer_text') and not data.get('answer_image'):
            raise serializers.ValidationError("Необходимо указать текст или изображение ответа.")
        return data

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Exam
        fields = '__all__'
