from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    '''Helper function to create new user'''
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    '''Test the users API (public)'''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        '''Test creating user with a valid payload is successful'''
        payload = {
            'email': 'test@recipeapp.com',
            'password': 'test123',
            'name': 'name',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(
            user.check_password(payload['password'])
        )
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        '''Test creating a user that already exists fails'''
        payload = {'email': 'test@recipeapp.com', 'password': 'test123'}
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # The reason to get bad request is we create user in line 42
        # but again in response we post the same payload.
        # Another thing to mention is that tests functions ar independent.
        # It does not matter, if we create user by same credintial.

    def test_password_too_short(self):
        '''Test that password must be more than 5 characters'''
        payload = {'email': 'test@recipeapp.com', 'password': 'pw'}
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
