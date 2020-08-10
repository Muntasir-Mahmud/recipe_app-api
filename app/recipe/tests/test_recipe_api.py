from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')
# reverse('app:url name')


def sample_recipe(user, **params):
    '''Create and return smaple recipe'''
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price_of_ingredient': 100.00
    }
    defaults.update(params)
    # If we pass params ,that will override
    # the defaults dictionary by update(params)
    # otherwise the object with default will create

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTest(TestCase):
    '''Test unauthenticated recipe API access'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that authentication is required'''
        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    '''Test unauthenticated recipe API access'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@recipe.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipe(self):
        '''Test retriving a list of recipes'''
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_recipe_limited_to_user(self):
        '''Test retrieving recipes for user'''
        user2 = get_user_model().objects.create_user(
            'other@recipe.com',
            'testpassword',
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)
