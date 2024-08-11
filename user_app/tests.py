from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from .models import CustomUser

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')

        self.user = CustomUser.objects.create_user(
            email='user@example.com',
            password='password123',
            first_name='User',
            last_name='User',
            initial_name='User',
        )

        self.coach = CustomUser.objects.create_coach(
            email='Coach@example.com',
            password='password123',
            first_name='Coach',
            last_name='Coach',
            initial_name='Coach',
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

    # Default user cant auth
    def test_user_cant_auth(self):
        data = {
            'email': 'user@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.data)

    

class UserDetailUpdateAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.staff = CustomUser.objects.create_user(
            email='staff@example.com',
            password='password123',
            first_name='User',
            last_name='Staff',
            initial_name='Test',
            is_staff=True,
        )

        self.coach1 = CustomUser.objects.create_coach(
            email='coach1@example.com',
            password='password123',
            first_name='User',
            last_name='Coach 1',
            initial_name='Test',
        )

        self.coach2 = CustomUser.objects.create_coach(
            email='coach2@example.com',
            password='password123',
            first_name='User',
            last_name='Coach 2',
            initial_name='Test',
        )

        self.staff_token = Token.objects.create(user=self.staff)
        self.coach1_token = Token.objects.create(user=self.coach1)
        self.coach2_token = Token.objects.create(user=self.coach2)

        self.url = reverse('user-detail-update', kwargs={'pk': self.coach1.pk})

    # def test_owner_can_retrieve_own_profile(self):
    #     self.client.login(email='coach1@example.com', password='password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['email'], self.coach1.email)

    # def test_owner_can_update_own_profile(self):
    #     self.client.login(email='coach1@example.com', password='password123')
    #     response = self.client.patch(self.url, {
    #         'email': 'coach1_updated@example.com',
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['email'], 'coach1_updated@example.com')

    # def test_other_user_cannot_update_owner_profile(self):
    #     self.client.login(email='coach2@example.com', password='password123')
    #     response = self.client.patch(self.url, {
    #         'email': 'coach1_updated@example.com',
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_staff_user_can_update_any_profile(self):
    #     self.client.login(email='staff@example.com', password='password123')
    #     response = self.client.patch(self.url, {
    #         'email': 'coach1_updated2@example.com',
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['email'], 'coach1_updated2@example.com')

    # def test_anonymous_user_can_retrieve_profile(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['email'], self.coach1.email)

    # def test_anonymous_user_cannot_update_profile(self):
    #     response = self.client.patch(self.url, {
    #         'email': 'coach1_updated3@example.com',
    #     })
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_retrieve_own_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.coach1_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.coach1.email)

    def test_owner_can_update_own_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.coach1_token.key)
        response = self.client.patch(self.url, {
            'email': 'coach1_updated@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'coach1_updated@example.com')

    def test_other_user_cannot_update_owner_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.coach2_token.key)
        response = self.client.patch(self.url, {
            'email': 'coach1_updated@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_update_any_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        response = self.client.patch(self.url, {
            'email': 'coach1_updated2@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'coach1_updated2@example.com')

    def test_anonymous_user_can_retrieve_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.coach1.email)

    def test_anonymous_user_cannot_update_profile(self):
        updated_data = {
        'email': 'coach1_updated@example.com',
        'first_name': 'UpdatedFirstName',
        'last_name': 'UpdatedLastName',
        'initial_name': 'UpdatedInitialName',
        'date_of_birth': '2000-01-01',
        'school': None,
        }

        response = self.client.put(self.url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(self.url, {
            'email': 'coach1_updated3@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)