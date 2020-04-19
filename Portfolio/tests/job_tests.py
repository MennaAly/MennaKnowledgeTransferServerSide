from model_mommy import mommy
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from Portfolio.models import Project, Job
from MasterData.models import ImplementationTool, Category
import json
import datetime


class JobTest(TestCase):
    def authorization_setup(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    def create_job_setup(self):
        self.projects = mommy.make(Project, _quantity=3)

    def setUp(self):
        self.authorization_setup()
        self.create_job_setup()

    def reverse_url(self, url, query_params_dict):
        return reverse(url, kwargs=query_params_dict)

    def test_create_job(self):
        request_data = {
            "company_name": "smart",
            "date_from": '2006-10-25',
            "date_to": '2007-10-25',
            "position_name": "software engineer",
            "project_ids": [self.projects[0].id, self.projects[1].id, self.projects[2].id],
            "responsibility": [{
                'name': 'res1'
            }, {
                'name': 'res2'
            }, {
                'name': 'res3'
            }, {
                'name': 'res4'
            }]
        }
        url = self.reverse_url("job-list", {})
        url += '?action=save'
        response = self.client.post(url, json.dumps(request_data),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Job.objects.count(), 1)
        created_job_instance = Job.objects.last()
        self.assertEqual(created_job_instance.projects.count(), 3)
        self.assertEqual(created_job_instance.responsibilities.count(), 4)
