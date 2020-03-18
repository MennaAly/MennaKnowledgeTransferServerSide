from rest_framework import serializers
from MasterData.models import ImplementationTool


class ImplementationToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImplementationTool
        fields = '__all__'
