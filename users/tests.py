from rest_framework.test import APITestCase
from users.models import User
from rest_framework import status
from django.urls import reverse

class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="testpassword",
            first_name="Иван",
            last_name="Иванов",
            role="STUDENT"
        )

    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('users:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
