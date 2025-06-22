from django.contrib import admin
from .models import Stream, StreamStudentResult

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam', 'created_by', 'created_at', 'stream_link')
    search_fields = ('name',)

@admin.register(StreamStudentResult)
class StreamStudentResultAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_surname', 'stream', 'total_score', 'total_time', 'passed_at')
    search_fields = ('student_name', 'student_surname')
