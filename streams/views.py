from rest_framework.permissions import IsAdminUser
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .serializers import StreamSerializer, StreamStudentResultSerializer
import os
import io
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Stream, StreamStudentResult

class StreamListCreateView(generics.ListCreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class StreamRetrieveView(generics.RetrieveAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticated]


class StreamStudentsListView(generics.ListAPIView):
    serializer_class = StreamStudentResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        stream_id = self.kwargs['stream_id']
        return StreamStudentResult.objects.filter(stream__id=stream_id)


class SubmitExamAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        stream_id = data.get("stream_id")
        stream = get_object_or_404(Stream, id=stream_id)

        StreamStudentResult.objects.create(
            stream=stream,
            full_name=data['full_name'],
            total_score=data['total_score'],
            total_time=data['total_time'],
            is_cheated=data.get('is_cheated', "")
        )
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)


FONT_PATH = os.path.join(settings.BASE_DIR, 'fonts', 'DejaVuSans.ttf')
pdfmetrics.registerFont(TTFont('DejaVu', FONT_PATH))

class StreamResultsPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, stream_id):
        cheated_only = request.query_params.get("cheated_only") == "true"
        stream = get_object_or_404(Stream, id=stream_id)

        results = StreamStudentResult.objects.filter(
            stream=stream,
            is_cheated__isnull=False if cheated_only else None
        )
        if cheated_only:
            results = results.exclude(is_cheated="")

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 50

        title = (
            f"Отчёт по списываниям (Поток: {stream.name})"
            if cheated_only else
            f"Результаты потока: {stream.name}"
        )

        p.setFont("DejaVu", 14)
        p.drawString(50, y, title)
        y -= 30

        p.setFont("DejaVu", 10)
        if not results.exists():
            p.drawString(50, y, "Нет данных.")
        else:
            for result in results:
                line = (
                    f"{result.full_name} | Баллы: {result.total_score} | "
                    f"Время: {result.total_time} мин | "
                    f"Списывал: {result.is_cheated or '—'}"
                )
                p.drawString(50, y, line)
                y -= 20
                if y < 50:
                    p.showPage()
                    p.setFont("DejaVu", 10)
                    y = height - 50

        p.save()
        buffer.seek(0)

        filename = f"{stream.name}_cheating_report.pdf" if cheated_only else f"{stream.name}_results.pdf"
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
