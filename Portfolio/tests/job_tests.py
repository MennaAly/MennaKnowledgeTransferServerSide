from datetime import datetime, date
from model_mommy import mommy
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from MasterData.models import Responsibility
from Portfolio.models import Project, Job
from helper import reverse_url, authorization_setup, create_request_body, create_dummy_instances, create_dummy_instance
import json


class CreateJobTest(TestCase):
    def create_job_setup(self):
        self.projects = create_dummy_instances(Project, 3, False)

    def setUp(self):
        self.client = authorization_setup()
        self.create_job_setup()

    def test_create_job(self):
        job_count = Job.objects.count()
        request_data = create_request_body({
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
        })
        url = reverse_url("job-list", {})
        url += '?action=save'
        response = self.client.post(url, request_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Job.objects.count(), job_count + 1)
        created_job_instance = Job.objects.last()
        self.assertEqual(created_job_instance.projects.count(), 3)
        self.assertEqual(created_job_instance.responsibilities.count(), 4)


class UpdateJobTest(TestCase):
    def update_job_setup(self):
        self.updated_job = create_dummy_instance(Job, True)
        print(self.updated_job)
        self.responsibilities = create_dummy_instances(Responsibility, 2, False)
        self.projects = create_dummy_instances(Project, 3, False)
        self.updated_job.projects.add(*self.projects)
        self.updated_job.responsibilities.add(*self.responsibilities)
        self.updated_job.save()
        self.update_url = reverse_url("job-detail", {'pk': self.updated_job.id})
        self.update_url += '?action=save'

    def setUp(self):
        self.client = authorization_setup()
        self.update_job_setup()

    def validate_update_job_end_date(self, date_to):
        self.assertEqual(Job.objects.filter(id=self.updated_job.id).first().date_to, date_to)

    def send_data_to_update_job_api(self, request_data):
        return self.client.put(self.update_url, request_data, content_type="application/json")

    def test_update_job_end_date(self):
        request_data = create_request_body({
            'id': self.updated_job.id,
            'date_to': '2008-10-25'
        })
        response = self.send_data_to_update_job_api(request_data)
        self.assertEqual(response.status_code, 200)
        self.validate_update_job_end_date(date(2008, 10, 25))

    def create_project_ids(self, projects_quantity):
        new_projects = create_dummy_instances(Project, projects_quantity, False)
        project_ids = []
        for i in range(0, projects_quantity):
            project_ids.append(new_projects[i].id)
        return project_ids

    def get_updated_job_projects_count(self):
        return Job.objects.filter(id=self.updated_job.id).first().projects.count()

    def validate_updated_job_projects_count(self, job_projects_count, new_count):
        self.assertEqual(Job.objects.filter(id=self.updated_job.id).first().projects.count(),
                         job_projects_count + new_count)

    def test_update_job_projects(self):
        new_projects_quantity = 2
        project_ids = self.create_project_ids(new_projects_quantity)
        job_projects_count = self.get_updated_job_projects_count()
        request_data = create_request_body({
            'id': self.updated_job.id,
            'project_ids': project_ids
        })
        response = self.send_data_to_update_job_api(request_data)
        self.assertEqual(response.status_code, 200)
        self.validate_updated_job_projects_count(job_projects_count, new_projects_quantity)
    #
    # def create_new_responsibilities(self, quantity):
    #     return mommy.make(Responsibility, _quantity=quantity)
    #
    # def get_update_job_responsibilities_count(self):
    #     return Job.objects.filter(id=self.updated_job.id).first().responsibilities.count()
    # def check_updated_job_responsibilities(self,job_responsibilities_count,new_count):
    #     self.assertEqual(Job.objects.filter(id=self.updated_job.id).first().responsibilities.count(),
    #                      job_responsibilities_count + new_count)
    # def test_update_job_responsibilities(self):
    #     new_responsibilities = self.create_new_responsibilities(2)
    #     job_responsibilities_count = self.get_update_job_responsibilities_count()
    #     request_data = json.dumps({
    #         'id': self.updated_job.id,
    #         'responsibility': [new_responsibilities[0].name, new_responsibilities[1].name]
    #     })
    #     url = self.reverse_url("job-list", {})
    #     url += '?action=save'
    #     response = self.client.put(url, request_data)
    #     self.assertEqual(response.status_code, 200)
    #
    #
    # def test_update_job_end_date_and_job_projects(self):
    #
    # def test_update_job_end_date_and_job_responsibilities(self):
    #
    # def test_update_job_projects_and_update_job_responsibilities(self):
    #
    # def test_update_job_end_date_and_job_projects_and_job_responsibilities(self):
