from rest_framework.test import APITestCase
from users.models import User
from exams.models import Exam
from streams.models import Stream

class StreamTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test3@test.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            role="TEACHER"
        )
        self.exam = Exam.objects.create(
            name="Экзамен",
            subject="Математика",
            total_questions=10,
            total_points=100,
            timer=60,
            is_microphone_required=False,
            created_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_stream(self):
        data = {"exam": self.exam.id, "name": "Поток 1"}
        response = self.client.post('/api/v1/streams/', data, format='json')
        self.assertEqual(response.status_code, 201)
