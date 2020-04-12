from rest_framework import serializers
from Portfolio.models import Job


class JobSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'company_name',
            'date_from',
            'date_to',
            'position_name'
        ]
