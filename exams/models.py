import uuid
from django.db import models
from users.models import User


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название экзамена")
    total_questions = models.IntegerField(verbose_name="Количество вопросов")
    total_points = models.IntegerField(verbose_name="Общее количество баллов")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создано пользователем")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_microphone_required = models.BooleanField(default=False, verbose_name="Требуется микрофон")
    timer = models.IntegerField(verbose_name="Время на экзамен (мин)")

    class Meta:
        verbose_name = "Экзамен"
        verbose_name_plural = "Экзамены"

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = (
        ('TP', 'Текстовое поле'),
        ('FT', 'Фотография'),
        ('IO', 'Интерактивный ответ'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', verbose_name="Экзамен")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="Тип вопроса")
    title = models.CharField(max_length=255, verbose_name="Заголовок вопроса")
    description = models.TextField(verbose_name="Описание")
    main_image = models.ImageField(upload_to='questions/', null=True, blank=True, verbose_name="Изображение (опционально)")
    score = models.IntegerField(verbose_name="Баллы за вопрос")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title


class AnswerOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    answer_text = models.TextField(null=True, blank=True, verbose_name="Текст ответа")
    answer_image = models.ImageField(upload_to='answers/', null=True, blank=True, verbose_name="Изображение ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.answer_text if self.answer_text else "🖼 Изображение"
