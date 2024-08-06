from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Coach, Athlete

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')

        # Creating users
        self.coach = Coach.objects.create_user(
            email='coach@example.com',
            password='password123',
            first_name='Test',
            last_name='Coach',
            date_of_birth='2000-01-01'
        )

        self.athlete = Athlete.objects.create_user(
            email='athlete@example.com',
            password='password123',
            first_name='Test',
            last_name='Athlete',
            date_of_birth='2000-01-01'
        )

    # Coach can auth test
    def test_coach_auth(self):
        data = {
            'email': 'coach@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    # Athlete cant auth test
    def test_athlete_unauth(self):
        data = {
            'email': 'athlete@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.data)

    