from rest_framework.test import APITestCase
from users.models import User
from exams.models import Exam

class ExamTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test2@test.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
            role="TEACHER"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_exam(self):
        data = {
            "name": "Тестовый экзамен",
            "total_questions": 5,
            "total_points": 50,
            "timer": 45,
            "is_microphone_required": False
        }
        response = self.client.post('/api/v1/exams/', data, format='json')
        self.assertEqual(response.status_code, 201)
