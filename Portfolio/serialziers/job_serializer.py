from rest_framework import serializers

from MasterData.serializers import ResponsibilitySerializer
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


class JobRetrieveSerializer(serializers.ModelSerializer):
    job_responsibilities = serializers.SerializerMethodField()

    def get_job_responsibilities(self, obj):
        responsibilities = Job.objects.filter(id=obj.id).first().responsibilities
        return ResponsibilitySerializer(responsibilities,many=True).data

    class Meta:
        model = Job
        fields = [
            'company_name',
            'date_from',
            'date_to',
            'position_name',
            'job_responsibilities'
        ]
