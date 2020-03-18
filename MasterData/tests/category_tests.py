from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from MasterData.models import Category
import json


class CategoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.add_category_url = reverse('MasterData:create-category')

    def test_add_category(self):
        response = self.client.post(self.add_category_url, data={'name': 'Backend'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 1)
