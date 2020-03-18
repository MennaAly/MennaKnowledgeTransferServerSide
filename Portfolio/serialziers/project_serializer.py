from rest_framework import serializers
from Portfolio.models import Project
from MasterData.models import ImplementationTool, Category
from MasterData.serializers import ImplementationToolSerializer, CategorySerializer


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'url',
            'github_url'
        ]


