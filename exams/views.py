import os
import uuid
from openai import OpenAI
import fitz  # PyMuPDF
from docx import Document

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import default_storage

from .models import Exam, Question, AnswerOption
from .serializers import ExamSerializer

client = OpenAI(api_key=settings.OPENAI_API_KEY)


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
        method = request.data.get("method")

        if method == "manual":
            return self.import_manual(request)
        elif method == "ai":
            return self.import_ai(request)
        elif method == "file":
            return self.import_file(request)
        else:
            return Response({"error": "Метод импорта не указан или неверен"}, status=400)

    def import_manual(self, request):
        data = request.data
        exam_data = data["exam"]
        questions_data = data["questions"]

        exam = Exam.objects.create(
            name=exam_data["name"],
            total_questions=exam_data["total_questions"],
            total_points=exam_data["total_points"],
            timer=exam_data["timer"],
            is_microphone_required=exam_data["is_microphone_required"],
            created_by=request.user
        )

        for q in questions_data:
            question = Question.objects.create(
                exam=exam,
                question_type=q["question_type"],
                title=q["title"],
                description=q["description"],
                score=q["score"]
            )
            for ans in q.get("answers", []):
                AnswerOption.objects.create(
                    question=question,
                    answer_text=ans["answer_text"],
                    is_correct=ans["is_correct"]
                )

        return Response({"status": "success"}, status=201)

    def import_ai(self, request):
        prompt = request.data.get("prompt")
        exam_name = request.data.get("name", "Экзамен ИИ")
        total_points = int(request.data.get("total_points", 10))
        timer = int(request.data.get("timer", 30))
        questions_count = int(request.data.get("total_questions", 5))

        if not prompt:
            return Response({"error": "Prompt обязателен"}, status=400)

        system_prompt = (
            f"Создай {questions_count} тестовых вопросов по следующей теме: {prompt}. "
            "Каждый вопрос с 4 вариантами ответа, один из которых верный. "
            "Формат ответа — JSON: список вопросов с title, description, score, answers (answer_text, is_correct)."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты генератор экзаменационных вопросов."},
                    {"role": "user", "content": system_prompt}
                ],
                temperature=0.7
            )
            result = response.choices[0].message.content
            questions = eval(result) if isinstance(result, str) else result

            exam = Exam.objects.create(
                name=exam_name,
                total_questions=questions_count,
                total_points=total_points,
                timer=timer,
                is_microphone_required=False,
                created_by=request.user
            )

            for q in questions:
                question = Question.objects.create(
                    exam=exam,
                    question_type="TP",
                    title=q["title"],
                    description=q.get("description", ""),
                    score=q.get("score", 2)
                )
                for ans in q["answers"]:
                    AnswerOption.objects.create(
                        question=question,
                        answer_text=ans["answer_text"],
                        is_correct=ans["is_correct"]
                    )

            return Response({"status": "AI exam created"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def import_file(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Файл обязателен"}, status=400)

        filename = default_storage.save(file.name, file)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        extension = filename.split('.')[-1].lower()

        try:
            if extension == "pdf":
                text = self.extract_text_from_pdf(file_path)
            elif extension in ["docx", "doc"]:
                text = self.extract_text_from_docx(file_path)
            else:
                return Response({"error": "Поддерживаются только PDF и DOCX"}, status=400)

            ai_request = request._request
            ai_request.data = {**request.data, "prompt": text}
            return self.import_ai(ai_request)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def extract_text_from_pdf(self, path):
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def extract_text_from_docx(self, path):
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
