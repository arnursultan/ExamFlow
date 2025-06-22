from django.contrib import admin
from .models import TeacherManual

@admin.register(TeacherManual)
class TeacherManualAdmin(admin.ModelAdmin):
    list_display = ('video_link',)
