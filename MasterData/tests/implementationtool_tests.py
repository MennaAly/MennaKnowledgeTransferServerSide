from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from MasterData.models import ImplementationTool
import json


class ImplementationToolTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.add_implementation_tool__url = reverse('MasterData:create-implementationtool')

    def test_add_implementation_tool(self):
        response = self.client.post(self.add_implementation_tool__url, data={'name': 'Backend'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ImplementationTool.objects.count(), 1)
