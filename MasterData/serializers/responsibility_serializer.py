from rest_framework import serializers
from MasterData.models import Responsibility


class ResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsibility
        fields = '__all__'
