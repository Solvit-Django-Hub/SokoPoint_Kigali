from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'StrongPassword123',
            'password_confirm': 'StrongPassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        """Ensure we can create a new user object."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_user_registration_password_mismatch(self):
        """Ensure password mismatch fails."""
        data = self.user_data.copy()
        data['password_confirm'] = 'WrongPassword123'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['errors'])

    def test_user_login(self):
        """Ensure user can login and get token."""
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            'email': 'testuser@example.com',
            'password': 'StrongPassword123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
