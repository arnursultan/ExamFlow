import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Stream, StreamStudentResult
from .serializers import StreamSerializer, StreamStudentResultSerializer


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


class StreamResultsPDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, stream_id):
        stream = get_object_or_404(Stream, id=stream_id)
        results = StreamStudentResult.objects.filter(stream=stream)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 50

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y, f"Результаты для потока: {stream.name}")
        y -= 30

        p.setFont("Helvetica", 12)
        for result in results:
            line = (
                f"{result.full_name} | Баллы: {result.total_score} | "
                f"Время: {result.total_time} мин | Списывал: {result.is_cheated or '—'}"
            )
            p.drawString(50, y, line)
            y -= 20
            if y < 50:
                p.showPage()
                y = height - 50

        p.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{stream.name}_results.pdf"'
        return response
