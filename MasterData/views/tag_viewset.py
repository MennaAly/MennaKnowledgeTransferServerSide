from rest_framework import viewsets, generics

from MasterData.models import Tag
from MasterData.serializers import TagSerializer


class TagViewSet(generics.CreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
