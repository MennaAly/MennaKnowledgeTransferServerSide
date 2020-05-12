from rest_framework import viewsets

from MasterData.models import Tag
from MasterData.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
