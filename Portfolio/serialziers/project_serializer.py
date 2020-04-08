from rest_framework import serializers
from Portfolio.models import Project
from MasterData.models import ImplementationTool, Category
from MasterData.serializers import ImplementationToolSerializer, CategorySerializer


class ProjectSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'url',
            'github_url'
        ]


class ProjectRetrieveSerializer(serializers.ModelSerializer):
    project_implementation_tools = serializers.SerializerMethodField()
    project_categories = serializers.SerializerMethodField()

    def get_project_implementation_tools(self, project):
        implementation_tool_instances = ImplementationTool.objects.filter(project=project)
        return ImplementationToolSerializer(implementation_tool_instances, many=True).data

    def get_project_categories(self, project):
        category_instances = Category.objects.filter(project=project)
        return CategorySerializer(category_instances, many=True).data

    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'url',
            'github_url',
            'created_date',
            'project_implementation_tools',
            'project_categories'
        ]
