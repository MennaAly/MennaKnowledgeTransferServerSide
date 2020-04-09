from model_mommy import mommy
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from Portfolio.models import Project
from MasterData.models import ImplementationTool, Category
import json
import datetime


class ProjectTest(TestCase):
    def create_projects_with_different_dates(self):
        self.project_in_year_2019 = Project(name="project2019", url="http://", github_url="http://bla",
                                            description="blabla", created_date=datetime.datetime(2019, 6, 1))
        self.project_in_year_2018 = Project(name="project2018", url="http://", github_url="http://bla",
                                            description="blabla", created_date=datetime.datetime(2018, 6, 1))
        self.project_in_year_2017 = Project(name="project2017", url="http://", github_url="http://bla",
                                            description="blabla", created_date=datetime.datetime(2017, 6, 1))
        self.project_in_year_2017.save()
        self.project_in_year_2018.save()
        self.project_in_year_2019.save()

    def retrieve_project_by_date_setup(self):
        self.create_projects_with_different_dates()

    def authorization_setup(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    def create_project_setup(self):
        self.first_dummy_category = mommy.make(Category)
        self.second_dummy_category = mommy.make(Category)
        self.first_dummy_implementation_tool = mommy.make(ImplementationTool)
        self.second_dummy_implementation_tool = mommy.make(ImplementationTool)

    def update_project_setup(self):
        self.saved_project = Project(name="project2015", url="http://", github_url="http://bla", description="blabla",
                                     created_date=datetime.datetime(2015, 6, 1))
        self.saved_project.save()

    def filter_project_by_category_setup(self):
        # first category
        self.project_in_year_2019.categories.add(self.first_dummy_category)
        self.project_in_year_2018.categories.add(self.first_dummy_category)
        self.saved_project.categories.add(self.first_dummy_category)
        # second category
        self.project_in_year_2017.categories.add(self.second_dummy_category)
        self.project_in_year_2017.save()
        self.project_in_year_2018.save()
        self.project_in_year_2019.save()
        self.saved_project.save()

    def filter_project_by_implementation_tools_setup(self):
        # first tool
        self.project_in_year_2019.implementation_tools.add(self.first_dummy_implementation_tool)
        self.saved_project.implementation_tools.add(self.first_dummy_implementation_tool)
        # second tool
        self.project_in_year_2017.implementation_tools.add(self.second_dummy_implementation_tool)
        self.project_in_year_2018.implementation_tools.add(self.second_dummy_implementation_tool)
        self.project_in_year_2017.save()
        self.project_in_year_2018.save()
        self.project_in_year_2019.save()
        self.saved_project.save()

    def reverse_url(self, url, query_params_dict):
        return reverse(url, kwargs=query_params_dict)

    def setUp(self):
        self.authorization_setup()
        self.create_project_setup()
        self.update_project_setup()
        self.retrieve_project_by_date_setup()
        self.filter_project_by_category_setup()
        self.filter_project_by_implementation_tools_setup()

    # def test_create_project(self):
    #     count_of_projects_before_insertion = Project.objects.count()
    #     url = self.reverse_url("project-list", {})
    #     url += '?action=save'
    #     response = self.client.post(url, data={
    #         "name": "SMS",
    #         "description": "medical insurance system",
    #         "url": "http://bla",
    #         "github_url": "htt://blabla",
    #         "implementation_tool_ids": [self.first_dummy_implementation_tool.id,
    #                                     self.second_dummy_implementation_tool.id],
    #         "category_ids": [self.first_dummy_category.id, self.second_dummy_category.id]
    #
    #     })
    #     self.assertEqual(Project.objects.count(), count_of_projects_before_insertion + 1)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_update_project(self):
    #     data = json.dumps({
    #         "name": "project1",
    #         "description": "medical insurance system",
    #         "url": "htpp://",
    #         "github_url": "http://bla",
    #     })
    #     url = self.reverse_url("project-detail", {"pk": self.saved_project.pk})
    #     url += "?action=save"
    #     response = self.client.put(url, data=data, content_type="application/json")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Project.objects.get(name="project1").description, "medical insurance system")
    #
    # def test_retrieve_project_by_date(self):
    #     url = self.reverse_url("project-list", {})
    #     url += "?ordering=-created_date&action=retrieve_by_date"
    #     response = self.client.get(url)
    #     response_returned_content = json.loads(response.content)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response_returned_content[0]['name'], "project2019")
    #     self.assertEqual(response_returned_content[len(response_returned_content) - 1]['name'], "project2015")

    def test_filter_project_by_category(self):
        url = self.reverse_url("project-list", {})
        url += "?categories__id=" + str(self.first_dummy_category.id)
        response = self.client.get(url)
        response_returned_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_returned_content), 3)
       
    def test_filter_project_by_implementation_tool(self):
        url = self.reverse_url("project-list", {})
        url += "?implementation_tools__id=" + str(self.first_dummy_implementation_tool.id)
        response = self.client.get(url)
        response_returned_content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_returned_content), 2)
