from rest_framework import status, viewsets, filters, pagination
from rest_framework.response import Response

from MasterData.serializers import ResponsibilitySerializer
from Portfolio.models import Job, Project
from Portfolio.serialziers.job_serializer import JobSaveSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    request_data = None
    job_serializer = None
    job_instance = None
    project_ids = None
    project_instances = None
    responsibility_dict_from_request = []
    responsibility_serializer = None
    responsibility_instances = None

    def get_queryset(self):
        action = self.request.query_params.get('action')
        if action == 'save':
            return Job.objects.only('company_name',
                                    'date_from',
                                    'date_to',
                                    'position_name')
        else:
            return Job.objects.all()

    def get_serializer_class(self):
        action = self.request.query_params.get('action')
        if action == 'save':
            return JobSaveSerializer

    def get_request_data(self):
        self.request_data = self.request.data

    def serialize_job(self):
        return JobSaveSerializer(data=self.request_data)

    def validate_serializer(self, serializer):
        serializer.is_valid(raise_exception=True)

    def save_serializer(self, serializer):
        return serializer.save()

    def create_job_instance(self):
        self.job_serializer = self.serialize_job()
        self.validate_serializer(self.job_serializer)
        self.job_instance = self.save_serializer(self.job_serializer)

    def get_project_ids_from_request(self):
        return self.request_data['project_ids']

    def get_project_instances(self):
        return Project.objects.filter(id__in=self.project_ids)

    def add_project_instances_to_job_instance(self):
        self.job_instance.projects.add(*self.project_instances)

    def save_job_instance(self):
        self.job_instance.save()

    def associate_projects_to_job(self):
        self.project_ids = self.get_project_ids_from_request()
        self.project_instances = self.get_project_instances()
        self.add_project_instances_to_job_instance()
        self.save_job_instance()

    def get_responsibility_from_request(self):
        return self.request_data['responsibility']

    def serialize_responsibilities(self):
        return ResponsibilitySerializer(data=self.responsibility_dict_from_request, many=True)

    def create_responsibility_instances(self):
        self.responsibility_dict_from_request = self.get_responsibility_from_request()
        self.responsibility_serializer = self.serialize_responsibilities()
        self.validate_serializer(self.responsibility_serializer)
        self.responsibility_instances = self.save_serializer(self.responsibility_serializer)

    def add_responsibility_instances_to_job_instance(self):
        self.job_instance.responsibilities.add(*self.responsibility_instances)

    def associate_responsibilities_to_job(self):
        self.add_responsibility_instances_to_job_instance()
        self.save_job_instance()

    def create(self, request, *args, **kwargs):
        self.get_request_data()
        self.create_job_instance()
        self.associate_projects_to_job()
        self.create_responsibility_instances()
        self.associate_responsibilities_to_job()
        return Response(status=status.HTTP_200_OK)

    def get_job_instance(self):
        self.job_instance = Job.objects.filter(id=self.request_data['id']).first()

    def update_job_end_date(self):
        if self.request_data.get('date_to', None) is not None:
            self.job_instance.date_to = self.request_data['date_to']
            self.save_job_instance()

    def update_job_projects(self):
        if self.request_data.get('project_ids', None) is not None:
            self.associate_projects_to_job()

    def update_job_responsibilities(self):
        if self.request_data.get('responsibility', None) is not None:
            self.create_responsibility_instances()
            self.associate_responsibilities_to_job()

    def update(self, request, *args, **kwargs):
        self.get_request_data()
        self.get_job_instance()
        self.update_job_end_date()
        self.update_job_projects()
        self.update_job_responsibilities()
        return Response(status=status.HTTP_200_OK)
