from model_mommy import mommy
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from Portfolio.models import Project
from MasterData.models import ImplementationTool, Category
import json


class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.first_dummy_category = mommy.make(Category)
        self.second_dummy_category = mommy.make(Category)
        self.first_dummy_implementation_tool = mommy.make(ImplementationTool)
        self.second_dummy_implementation_tool = mommy.make(ImplementationTool)
        self.project_url = reverse("project-list")
        self.saved_project = Project(name="project1", url="http://", github_url="http://bla", description="blabla")
        self.saved_project.save()
        print(self.saved_project.pk)
        self.project_detail_url = reverse("project-detail", kwargs={'pk': self.saved_project.id})

    def test_create_project(self):
        # print(type(self.first_dummy_category.id))
        # pass
        response = self.client.post(self.project_url, data={

            "name": "SMS",
            "description": "medical insurance system",
            "url": "http://bla",
            "github_url": "htt://blabla",
            "implementation_tool_ids": [self.first_dummy_implementation_tool.id,
                                        self.second_dummy_implementation_tool.id],
            "category_ids": [self.first_dummy_category.id, self.second_dummy_category.id]

        })
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(response.status_code, 200)

    def test_update_project(self):
        data = json.dumps({
            "name": "project1",
            "description": "medical insurance system",
            "url": "htpp://",
            "github_url": "http://bla",
            })
        response = self.client.put(self.project_detail_url,data=data,content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Project.objects.get(name="project1").description, "medical insurance system")
