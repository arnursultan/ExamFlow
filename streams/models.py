import uuid
from django.db import models
from exams.models import Exam
from users.models import User

class Stream(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="Экзамен")
    name = models.CharField(max_length=255, verbose_name="Название потока")
    stream_link = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name="Ссылка на поток (UUID)")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создано пользователем")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"

    def __str__(self):
        return f"Поток {self.name}"

class StreamStudentResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='results', verbose_name="Поток")
    student_name = models.CharField(max_length=255, verbose_name="Имя студента")
    student_surname = models.CharField(max_length=255, verbose_name="Фамилия студента")
    total_score = models.IntegerField(verbose_name="Общее количество баллов")
    total_time = models.IntegerField(verbose_name="Время прохождения (мин)")
    passed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата сдачи")

    class Meta:
        verbose_name = "Результат студента"
        verbose_name_plural = "Результаты студентов"

    def __str__(self):
        return f"{self.student_name} {self.student_surname} - {self.total_score} баллов"
