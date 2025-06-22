from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Exam, Question, AnswerOption
from .serializers import ExamSerializer

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ExamRetrieveView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExamImportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        exam_data = data['exam']
        questions_data = data['questions']

        exam = Exam.objects.create(
            name=exam_data['name'],
            total_questions=exam_data['total_questions'],
            total_points=exam_data['total_points'],
            timer=exam_data['timer'],
            is_microphone_required=exam_data['is_microphone_required'],
            created_by=request.user
        )

        for q in questions_data:
            question = Question.objects.create(
                exam=exam,
                question_type=q['question_type'],
                title=q['title'],
                description=q['description'],
                score=q['score']
            )
            for ans in q.get('answers', []):
                AnswerOption.objects.create(
                    question=question,
                    answer_text=ans['answer_text'],
                    is_correct=ans['is_correct']
                )

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
