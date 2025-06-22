import uuid
from django.db import models
from users.models import User


class TeacherManual(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    video_link = models.URLField(verbose_name="Ссылка на видео")
    audio_kg = models.FileField(upload_to='manuals/', verbose_name="Аудио (Кыргызский)")
    audio_uz = models.FileField(upload_to='manuals/', verbose_name="Аудио (Узбекский)")
    audio_ru = models.FileField(upload_to='manuals/', verbose_name="Аудио (Русский)")

    class Meta:
        verbose_name = "Справочник учителя"
        verbose_name_plural = "Справочники учителей"

    def __str__(self):
        return f"Справочник {self.id}"


class StudentProfile(models.Model):
    LANGUAGE_CHOICES = [
        ('kg', 'Кыргызский'),
        ('ru', 'Русский'),
        ('uz', 'Узбекский'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    bio = models.TextField(blank=True, verbose_name="О себе")
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru', verbose_name="Язык интерфейса")

    class Meta:
        verbose_name = "Профиль студента"
        verbose_name_plural = "Профили студентов"

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.language})"
