from datetime import datetime, date
from django.test import TestCase, Client
from model_mommy import mommy

from MasterData.models import Responsibility
from MasterData.serializers import ResponsibilitySerializer
from Portfolio.models import Project, Job
from Portfolio.serialziers.job_serializer import JobRetrieveSerializer
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

    def get_list_of_project_ids(self, projects_quantity):
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
        project_ids = self.get_list_of_project_ids(new_projects_quantity)
        job_projects_count = self.get_updated_job_projects_count()
        request_data = create_request_body({
            'id': self.updated_job.id,
            'project_ids': project_ids
        })
        response = self.send_data_to_update_job_api(request_data)
        self.assertEqual(response.status_code, 200)
        self.validate_updated_job_projects_count(job_projects_count, new_projects_quantity)

    def create_new_responsibilities_instances(self, quantity):
        return create_dummy_instances(Responsibility, quantity, False)

    def get_update_job_responsibilities_count(self):
        return Job.objects.filter(id=self.updated_job.id).first().responsibilities.count()

    def check_updated_job_responsibilities(self, job_responsibilities_count, new_count):
        self.assertEqual(Job.objects.filter(id=self.updated_job.id).first().responsibilities.count(),
                         job_responsibilities_count + new_count)

    def get_dict_of_responsibility_names(self, new_responsibilities_count):
        new_responsibilities = self.create_new_responsibilities_instances(new_responsibilities_count)
        responsibility_names = []
        for new_responsibility in new_responsibilities:
            responsibility_names.append({"name": new_responsibility.name})
        return responsibility_names

    def validate_updated_job_responsibilities_count(self, old_job_responsibilities_count,
                                                    new_job_responsibilities_count):
        self.assertEqual(Job.objects.filter(id=self.updated_job.id).first().responsibilities.count(),
                         old_job_responsibilities_count + new_job_responsibilities_count)

    def test_update_job_responsibilities(self):
        new_responsibilities_count = 2
        responsibility_names = self.get_dict_of_responsibility_names(new_responsibilities_count)
        job_responsibilities_count = self.get_update_job_responsibilities_count()
        request_data = json.dumps({
            'id': self.updated_job.id,
            'responsibility': responsibility_names
        })
        response = self.send_data_to_update_job_api(request_data)
        self.assertEqual(response.status_code, 200)
        self.validate_updated_job_responsibilities_count(job_responsibilities_count, new_responsibilities_count)

    def test_update_job_end_date_and_job_projects(self):
        new_projects_quantity = 2
        project_ids = self.get_list_of_project_ids(new_projects_quantity)
        job_projects_count = self.get_updated_job_projects_count()
        request_data = create_request_body({
            'id': self.updated_job.id,
            'date_to': '2009-10-25',
            'project_ids': project_ids
        })
        response = self.send_data_to_update_job_api(request_data)
        self.assertEqual(response.status_code, 200)
        self.validate_update_job_end_date(date(2009, 10, 25))
        self.validate_updated_job_projects_count(job_projects_count, new_projects_quantity)

    def test_update_job_end_date_and_job_responsibilities(self):
        new_responsibilities_count = 2
        responsibility_names = self.get_dict_of_responsibility_names(new_responsibilities_count)
        job_responsibilities_count = self.get_update_job_responsibilities_count()
        request_data = create_request_body({
            'id': self.updated_job.id,
            'date_to': '2010-10-25',
            'responsibility': responsibility_names
        })
        response = self.send_data_to_update_job_api(request_data)
        self.assertEqual(response.status_code, 200)
        self.validate_update_job_end_date(date(2010, 10, 25))
        self.validate_updated_job_responsibilities_count(job_responsibilities_count, new_responsibilities_count)

    def test_update_job_projects_and_update_job_responsibilities(self):
        new_projects_quantity = 2
        new_responsibilities_count = 2
        project_ids = self.get_list_of_project_ids(new_projects_quantity)
        job_projects_count = self.get_updated_job_projects_count()
        responsibility_names = self.get_dict_of_responsibility_names(new_responsibilities_count)
        job_responsibilities_count = self.get_update_job_responsibilities_count()
        request_data = json.dumps({
            'id': self.updated_job.id,
            'responsibility': responsibility_names,
            'project_ids': project_ids
        })
        response = self.send_data_to_update_job_api(request_data)
        self.assertEqual(response.status_code, 200)
        self.validate_updated_job_projects_count(job_projects_count, new_projects_quantity)
        self.validate_updated_job_responsibilities_count(job_responsibilities_count, new_responsibilities_count)

    def test_update_job_end_date_and_job_projects_and_job_responsibilities(self):
        new_projects_quantity = 2
        new_responsibilities_count = 2
        project_ids = self.get_list_of_project_ids(new_projects_quantity)
        job_projects_count = self.get_updated_job_projects_count()
        responsibility_names = self.get_dict_of_responsibility_names(new_responsibilities_count)
        job_responsibilities_count = self.get_update_job_responsibilities_count()
        request_data = json.dumps({
            'id': self.updated_job.id,
            'responsibility': responsibility_names,
            'project_ids': project_ids,
            'date_to': '2011-10-25',
        })
        response = self.send_data_to_update_job_api(request_data)
        self.assertEqual(response.status_code, 200)
        self.validate_update_job_end_date(date(2011, 10, 25))
        self.validate_updated_job_projects_count(job_projects_count, new_projects_quantity)
        self.validate_updated_job_responsibilities_count(job_responsibilities_count, new_responsibilities_count)


class RetrieveJobTest(TestCase):
    def retrieve_job_setup(self):
        self.retrieved_job = create_dummy_instance(Job, True)
        self.responsibilities = create_dummy_instances(Responsibility, 2, False)
        self.projects = create_dummy_instances(Project, 3, False)
        self.retrieved_job.projects.add(*self.projects)
        self.retrieved_job.responsibilities.add(*self.responsibilities)
        self.retrieved_job.save()
        self.retrieve_job_url = reverse_url("job-detail", {'pk': self.retrieved_job.id})
        self.retrieve_job_url += '?action=retrieve'

    def setUp(self):
        # no authorization
        # self.client = authorization_setup()
        self.client = Client()
        self.retrieve_job_setup()

    def send_data_to_update_job_api(self):
        return self.client.get(self.retrieve_job_url, content_type="application/json")

    def get_serialized_job(self):
        return JobRetrieveSerializer(self.retrieved_job).data

    def test_retrieve_job(self):
        response = self.send_data_to_update_job_api()
        response_returned_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_returned_content, self.get_serialized_job())


class RetrieveJobsByBeginDateTest(TestCase):
    def retrieve_jobs_setup(self):
        self.job_begin_in_2019 = mommy.make(Job, date_from=datetime(2019, 6, 1))
        self.job_begin_in_2020 = mommy.make(Job, date_from=datetime(2020, 6, 1))
        self.job_begin_in_2021 = mommy.make(Job, date_from=datetime(2021, 6, 1))
        self.job_begin_in_2022 = mommy.make(Job, date_from=datetime(2022, 6, 1))
        self.ordered_jobs_by_begin_date = Job.objects.order_by('-date_from')
        self.serialized_ordered_jobs_by_begin_date = JobRetrieveSerializer(self.ordered_jobs_by_begin_date,
                                                                           many=True).data
        self.retrieve_jobs_url = reverse_url("job-list", {})
        self.retrieve_jobs_url += '?action=retrieve&ordering=-date_from'

    def send_data_to_update_job_api(self):
        return self.client.get(self.retrieve_jobs_url, content_type="application/json")

    def setUp(self):
        # no authorization
        # self.client = authorization_setup()
        self.client = Client()
        self.retrieve_jobs_setup()

    def test_retrieve_jobs_by_begin_date(self):
        response = self.send_data_to_update_job_api()
        response_returned_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_returned_content, self.serialized_ordered_jobs_by_begin_date)
