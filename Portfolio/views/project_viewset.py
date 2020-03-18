from rest_framework import status, viewsets
from Portfolio.models import Project

class ProjectViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.action == 'get':

    def get_serializer_class(self):