from rest_framework import generics
from MasterData.models import ImplementationTool
from MasterData.serializers import ImplementationToolSerializer


class ImplementationToolViewSet(generics.CreateAPIView):
    queryset = ImplementationTool.objects.all()
    serializer_class = ImplementationToolSerializer
