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


