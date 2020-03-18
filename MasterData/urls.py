from django.conf.urls import url, include
from rest_framework import routers
from MasterData.views import CategoryViewSet, ImplementationToolViewSet

router = routers.SimpleRouter()
app_name = 'MasterData'
urlpatterns = [
    url(r'add_category', CategoryViewSet.as_view(), name='create-category'),
    url(r'add_implementation_tool', ImplementationToolViewSet.as_view(), name='create-implementationtool')
]
