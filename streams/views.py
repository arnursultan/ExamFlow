from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Stream, StreamStudentResult
from .serializers import StreamSerializer, StreamStudentResultSerializer
from exams.models import Exam
from django.shortcuts import get_object_or_404

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
            student_name=data['student_name'],
            student_surname=data['student_surname'],
            total_score=data['total_score'],
            total_time=data['total_time'],
            is_cheated=data['is_cheated']
        )
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
