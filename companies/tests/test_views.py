from django.contrib.auth import get_user_model
from rest_framework.test import (
    APITestCase,
    APIClient
)
from rest_framework import status

class CompanyViewTest(APITestCase):

    def setUp(self):
        self.base_url = '/api/v1/companies'
        self.user = get_user_model().objects.create_user(
            email = 'test@test.com',
            password = 'test1234#'
        )
        self.login_url = '/api/v1/auth/login/'
        response = self.client.post(
            self.login_url,
            {
                'email': 'test@test.com',
                'password': 'test1234#'
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {response.data["access"]}')


    def test_create_company(self):
        """ Verifica que la vista cree una empresa correctamente. """
        data = {
            'name': 'Tech Corp 2',
            'phone': '3012342340',
            'email': 'tech@email.com',
            'address': 'CL 46 N # 9AN',
            'nui': '88380000'
        }
        response = self.client.post(
            self.base_url,
            data = data,
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['phone'], data['phone'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['address'], data['address'])
        self.assertEqual(response.data['nui'], data['nui'])