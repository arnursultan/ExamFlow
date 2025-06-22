from django.contrib import admin
from .models import Stream, StreamStudentResult

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam', 'created_by', 'created_at', 'stream_link')
    search_fields = ('name',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'stream_link')


@admin.register(StreamStudentResult)
class StreamStudentResultAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'stream', 'total_score',
        'total_time', 'is_cheated', 'passed_at'
    )
    list_filter = ('is_cheated', 'passed_at')
    search_fields = ('full_name',)
    readonly_fields = ('passed_at',)
