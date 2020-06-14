from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response
from MasterData.models import ImplementationTool, Category
from Portfolio.models import Project
from Portfolio.serialziers import ProjectSaveSerializer
from rest_framework import filters
from Portfolio.serialziers.project_serializer import ProjectRetrieveSerializer
from django_filters import FilterSet, CharFilter, NumberFilter


class ProjectFilterClass(FilterSet):
    class Meta:
        model = Project
        fields = {'implementation_tools__id': ('exact',), 'categories__id': ('exact',), }


class ProjectViewSet(viewsets.ModelViewSet):
    created_project = None
    implementation_tool_instances = None
    category_instances = None
    request_data = None
    queryset = Project.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_date']
    # filter_fields = ('implementation_tools', 'categories',)
    filter_class = ProjectFilterClass

    def get_queryset(self):
        if self.request.query_params.get('action') == 'save':
            return Project.objects.all().only('name', 'description', 'url', 'github_url', 'created_date')
        elif self.request.query_params.get('action') == 'retrieve_by_date':
            return Project.objects.prefetch_related('implementation_tools', 'categories').only('name', 'description',
                                                                                               'url', 'github_url',
                                                                                               'created_date',
                                                                                               'implementation_tools__name',
                                                                                               'implementation_tools__id',
                                                                                               'categories__name',
                                                                                               'categories__id')
        else:
            return Project.objects.all()

    def get_serializer_class(self):
        if self.request.query_params.get('action') == 'save':
            return ProjectSaveSerializer
        elif self.request.query_params.get('action') == 'retrieve_by_date':
            return ProjectRetrieveSerializer
        else:
            return ProjectSaveSerializer

    def get_request_data(self):
        self.request_data = self.request.data

    def serialize_project_using_save_serializer(self):
        # project_json_from_request = self.request_data['project']
        return ProjectSaveSerializer(data=self.request_data)

    def validate_serializer(self, serializer):
        serializer.is_valid(raise_exception=True)

    def save_project_through_serializer_layer(self, project_serializer):
        return project_serializer.save()

    def create_project_instance(self):
        project_serializer = self.serialize_project_using_save_serializer()
        self.validate_serializer(project_serializer)
        self.created_project = self.save_project_through_serializer_layer(project_serializer)

    def get_implentation_tool_ids_from_request(self):
        implementation_tool_ids = self.request_data['implementation_tool_ids']
        return implementation_tool_ids

    def get_implementaion_tool_instances(self, implementation_tool_ids):
        return ImplementationTool.objects.filter(
            id__in=implementation_tool_ids
        )

    def add_implementation_tools_to_project(self):
        self.created_project.implementation_tools.add(*self.implementation_tool_instances)

    def save_project_through_data_base_layer(self):
        self.created_project.save()

    def associate_project_with_its_implementation_tools(self):
        implementation_tool_ids = self.get_implentation_tool_ids_from_request()
        self.implementation_tool_instances = self.get_implementaion_tool_instances(implementation_tool_ids)
        self.add_implementation_tools_to_project()
        self.save_project_through_data_base_layer()

    def get_category_ids_from_request(self):
        categories_ids = self.request_data['category_ids']
        return categories_ids

    def get_category_instances(self, categories_ids):
        return Category.objects.filter(id__in=categories_ids)

    def add_categories_to_project(self):
        self.created_project.categories.add(*self.category_instances)

    def associate_project_with_its_categories(self):
        categories_ids = self.get_category_ids_from_request()
        self.category_instances = self.get_category_instances(categories_ids)
        self.add_categories_to_project()
        self.save_project_through_data_base_layer()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        self.get_request_data()
        self.create_project_instance()
        self.associate_project_with_its_implementation_tools()
        self.associate_project_with_its_categories()
        return Response(status=status.HTTP_200_OK)
