from django.contrib import admin
from .models import Exam, Question, AnswerOption

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_questions', 'total_points', 'created_by', 'created_at')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_type', 'exam', 'score', 'created_at')
    list_filter = ('question_type',)
    search_fields = ('title',)

@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text', 'is_correct')
    list_filter = ('is_correct',)
