from __future__ import unicode_literals
from rest_framework import status, viewsets, filters, pagination
from rest_framework.response import Response
from Portfolio.models import Profile
from Portfolio.serialziers import ProfileSeraizler


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()

    def create(self, request, *args, **kwargs):
        profile_data = self.request.data
        profile_serializer = ProfileSeraizler(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        return Response(status=status.HTTP_200_OK)
