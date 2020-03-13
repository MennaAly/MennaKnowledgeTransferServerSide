from rest_framework import serializers
from Portfolio.models import Profile


class ProfileSeraizler(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
