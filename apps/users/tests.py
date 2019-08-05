from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


class RegistrationTest(APITestCase):

    def setUp(self):
        self.url = reverse('auth:register')

    def test_registration(self):
        valid_registration = {
            "username": "testuser",
            "password": "testpassword",
            "email": "testemail@testmail.com",
            "phone_number": "09398729312",
        }
        response = self.client.post(
            self.url,
            valid_registration
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Invalid status code.')
        self.assertEqual(response.data['username'], valid_registration['username'], 'Invalid username')
        self.assertEqual(response.data['email'], valid_registration['email'], 'Invalid email')
        self.assertEqual(response.data['phone_number'], valid_registration['phone_number'], 'Invalid phone number')
        self.assertTrue('token' in response.data, 'Token not found')

    def test_invalid_registration(self):
        invalid_registration = {
            "username": "testusa",
            "password": "testpa",
            "email": "testermail@testmail.com",
            "phone_number": "08936589654",
        }

        response = self.client.post(
            self.url,
            invalid_registration
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Invalid status code')


class LoginTest(APITestCase):

    def setUp(self):
        self.url = reverse('auth:login')
        self.username = 'testuser'
        self.password = '123456789'
        self.email = 'test@testmail.com'
        self.phone_number = '09213176895'
        User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
            phone_number=self.phone_number
        )

    def test_valid_login(self):
        valid_login = {
            'username': self.username,
            'password': self.password,
        }

        response = self.client.post(
            self.url,
            valid_login
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Invalid status code')
        self.assertEqual(response.data['username'], self.username, 'Invalid username')
        self.assertTrue('token' in response.data, 'Token not found')

    def test_invalid_login(self):
        invalid_login = {
            'username': self.username,
            'password': 'supersecurepassword',
        }
        response = self.client.post(
            self.url,
            invalid_login
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Invalid status code')

    def test_no_password_login(self):
        invalid_login = {
            'username': self.username,
        }

        response = self.client.post(
            self.url,
            invalid_login
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Invalid status code')


class UserTest(APITestCase):

    def setUp(self):
        self.url = reverse('auth:user')
        self.username = 'testuser'
        self.password = '123456789'
        self.email = 'test@testmail.com'
        self.phone_number = '09213176895'
        user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email,
            phone_number=self.phone_number
        )
        self.token = user.token

    def test_valid_user(self):

        valid_response = {
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Invalid status code')
        self.assertEqual(response.data, valid_response, 'Invalid response')

    def test_invalid_user(self):
        invalid_token = 'notatokenirepeatnotatoken'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + invalid_token)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'Invalid status code')

    def test_logged_out_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Invalid status code')

    def test_update_logged_in_user_valid_data(self):
        valid_request = {
            'username': self.username,
            'password': self.password,
            'email': 'testinio@testmail.com',
            'phone_number': self.phone_number
        }
        valid_response = {
            'username': self.username,
            'email': valid_request['email'],
            'phone_number': self.phone_number
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(
            self.url,
            valid_request
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Invalid status code')
        self.assertEqual(response.data, valid_response, 'Invalid response')

    def test_update_invalid_field(self):
        invalid_request = {
            'username': 'newusername',
            'password': self.password,
            'email': self.email,
            'phone_number': self.phone_number
        }
        valid_response = {
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(
            self.url,
            invalid_request
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Invalid status_code')
        self.assertEqual(response.data, valid_response, 'Invalid response')
