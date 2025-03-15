from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

class AuthenticationTests(APITestCase):

    def setUp(self):
        """ Configuración de datos para la prueba. """
        self.user = get_user_model().objects.create_user(
            email = 'test@test.com',
            password = 'test1234#'
        )
        self.login_url = '/api/v1/auth/login/'
        self.refresh_url = '/api/v1/auth/refresh/'
        self.verify_url = '/api/v1/auth/verify/'

    def test_login_successful(self):
        """ 
        Prueba para verificar que el login devuelve el 
        token de acceso y de refresco.
        """
        response = self.client.post(
            self.login_url,
            {
                'email': 'test@test.com',
                'password': 'test1234#'
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]


    def test_login_invalid_credentials(self):
        """ 
        Prueba para verificar que el login falla con 
        credenciales incorrectas.
        """
        response = self.client.post(
            self.login_url, 
            {
                'email': 'invalid@test.com', 
                'password': 'password'
            }, 
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_successful(self):
        """ 
        Prueba para verificar que el token refresh funciona correctamente. 
        """
        response = self.client.post(
            self.login_url,
            {
                'email': 'test@test.com',
                'password': 'test1234#'
            },
            format = 'json'
        )
        refresh_token = response.data["refresh"]
        response = self.client.post(
            self.refresh_url, 
            {
                'refresh': refresh_token
            }, 
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_verify_token_successful(self):
        """ 
        Prueba para verificar que el token de acceso es válido.
        """
        response = self.client.post(
            self.login_url,
            {
                'email': 'test@test.com',
                'password': 'test1234#'
            },
            format = 'json'
        )
        access_token = response.data["access"]
        response = self.client.post(
            self.verify_url, 
            {
                'token': access_token
            }, 
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token_invalid(self):
        """ 
        Prueba para verificar que un token inválido falla 
        en la verificación.
        """
        response = self.client.post(
            self.verify_url, 
            {
                'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyMDU3MjAyLCJpYXQiOjE3NDIwNTY4MjksImp0aSI6ImRhYjc1NzUwM2E0YTRiMGY4NWExYzM3NmVjYzZjZTQ1IiwidXNlcl9pZCI6MX0.NFloWOOeMh6hklqYwFsy_ydAD2m4FJXvk1BGzHrzdSA'
            }, 
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
