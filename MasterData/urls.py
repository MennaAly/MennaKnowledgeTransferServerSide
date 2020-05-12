from django.conf.urls import url, include
from rest_framework import routers
from MasterData.views import CategoryViewSet, ImplementationToolViewSet , TagViewSet

router = routers.SimpleRouter()
app_name = 'MasterData'
urlpatterns = [
    url(r'add_category', CategoryViewSet.as_view(), name='create-category'),
    url(r'add_implementation_tool', ImplementationToolViewSet.as_view(), name='create-implementationtool'),
    url(r'tag', TagViewSet.as_view(), name='create-tag')
]
