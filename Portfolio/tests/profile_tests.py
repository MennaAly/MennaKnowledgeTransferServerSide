from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from Portfolio.models import Profile

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.create_profile_url = reverse("profile-list")

    def test_create_profile(self):
        response = self.client.post(self.create_profile_url, data={
            "name": "Menna Ali",
            "description": "I'm a passionate Software engineer",
            "email": "mennaali365@gmail.com",
            "github_account": "github/Menna",
            "linkdin_account": "linkdin/Menna",
            "about": "bla bla"
        })
        self.assertEqual(response.status_code,200)
        self.assertEqual(Profile.objects.count(),1)
