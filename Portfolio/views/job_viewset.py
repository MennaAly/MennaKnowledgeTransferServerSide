from rest_framework import status, viewsets, filters, pagination
from rest_framework.response import Response
from Portfolio.models import Job
from Portfolio.serialziers.job_serializer import JobSaveSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job
    def get_queryset(self):
        action  = self.request.query_params.get('action')
        if action == 'save':
            return Job.objects.only( 'company_name',
            'date_from',
            'date_to',
            'position_name')
        else:
            return Job.objects.all()

    def get_serializer_class(self):
        action  = self.request.query_params.get('action')
        if action == 'save':
            return JobSaveSerializer

    def create(self, request, *args, **kwargs):
