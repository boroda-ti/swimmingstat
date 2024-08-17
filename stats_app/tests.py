from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from user_app.models import CustomUser

from .models import Athlete 

class AthleteCRUDTestCase(APITestCase):

    def setUp(self):

        self.client = APIClient()

        self.coach = CustomUser.objects.create_coach(
            email='coach@example.com',
            password='password123',
            first_name='User',
            last_name='Coach',
            initial_name='Test',
        )

        self.athlete1 = Athlete.objects.create(
            first_name = 'Athlete 1',
            last_name = 'Athlete 1',
            initial_name = 'Test',
            date_of_birth = '2006-02-20',
            rank = '3Y',
            coach = self.coach
        )

        self.athlete2 = Athlete.objects.create(
            first_name = 'Athlete 2',
            last_name = 'Athlete 2',
            initial_name = 'Test',
            date_of_birth = '2000-11-04',
            rank = '1A',
        )

        self.coach_token = Token.objects.create(user=self.coach)

        self.athlete_list_url = reverse('athlete-list')
        self.athlete_detail_url = reverse('athlete-detail', kwargs={'pk': self.athlete1.pk})

    # GET method
    def test_anonymous_user_can_read(self):
        response = self.client.get(self.athlete_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.athlete_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # POST method
    def test_coach_can_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.coach_token.key)
        data = {
            'first_name' : 'Athlete 3',
            'last_name' : 'Athlete 3',
            'initial_name' : 'Test',
            'date_of_birth' : '2001-06-29',
            'rank' : 'CMS',
            'coach' : self.coach.id
        }

        response = self.client.post(self.athlete_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], data['first_name'])

    def test_anonymous_user_cant_create(self):
        data = {
            'first_name' : 'Athlete 3',
            'last_name' : 'Athlete 3',
            'initial_name' : 'Test',
            'date_of_birth' : '2001-06-29',
            'rank' : 'CMS',
            'coach' : self.coach.id
        }

        response = self.client.post(self.athlete_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #PATCH method
    def test_coach_can_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.coach_token.key)
        data = {
            'first_name' : 'Athlete 3 updated',
        }

        response = self.client.patch(self.athlete_detail_url, data)
        self.athlete1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], data['first_name'])

    def test_anonymous_user_cant_update(self):
        data = {
            'first_name' : 'Athlete 3 updated',
        }

        response = self.client.post(self.athlete_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #DELETE method
    def test_coach_can_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.coach_token.key)
        response = self.client.delete(self.athlete_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_user_cant_delete(self):
        response = self.client.delete(self.athlete_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)