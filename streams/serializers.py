from rest_framework import serializers
from .models import Stream, StreamStudentResult

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = '__all__'
        read_only_fields = ('stream_link', 'created_by', 'created_at')

class StreamStudentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamStudentResult
        fields = '__all__'
        read_only_fields = ('passed_at',)
