from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from Portfolio.models import Profile
import json


class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.saved_profile = Profile(name="Youmna Ali", description="I'm a passionate Translater",
                                     email="youmnaali@gmail.com",
                                     github_account="github/youmna", linkdin_account="linkdin/youmna", about="blabla")
        self.saved_profile.save()
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.profile_url = reverse("profile-list")
        self.profile_detail_url = reverse("profile-detail", kwargs={'pk': self.saved_profile.pk})

    def test_create_profile(self):
        response = self.client.post(self.profile_url, data={
            "name": "Menna Ali",
            "description": "I'm a passionate Software engineer",
            "email": "mennaali365@gmail.com",
            "github_account": "github/Menna",
            "linkdin_account": "linkdin/Menna",
            "about": "bla bla"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Profile.objects.count(), 2)

    def test_update_profile(self):
        data = json.dumps({
            "name": "Youmna Ali",
            "description": "I'm a passionate Translater",
            "email": "youmnaali11@gmail.com",
            "github_account": "github/youmna",
            "linkdin_account": "linkdin/youmna",
            "about": "bla bla"
        })
        response = self.client.put(self.profile_detail_url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Profile.objects.get(name="Youmna Ali").email, "youmnaali11@gmail.com")

    def test_retrieve_profile(self):
        response = self.client.get(self.profile_detail_url)
        response_returned_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_returned_content['name'], "Youmna Ali")
