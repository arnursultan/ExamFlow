from django.contrib import admin
from .models import TeacherManual, StudentProfile


@admin.register(TeacherManual)
class TeacherManualAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_link')
    search_fields = ('video_link',)
    ordering = ('-id',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'language')
    search_fields = ('user__email', 'user__full_name')
    list_filter = ('language',)
