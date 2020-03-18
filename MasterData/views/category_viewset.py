from rest_framework import generics
from MasterData.models import Category
from MasterData.serializers import CategorySerializer

class CategoryViewSet(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
