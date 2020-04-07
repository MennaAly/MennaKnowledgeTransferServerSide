from django.conf.urls import url, include
from rest_framework import routers
from Portfolio.views import ProfileViewSet, ProjectViewSet

router = routers.SimpleRouter()

router.register(r'profile', ProfileViewSet)
router.register(r'project',ProjectViewSet)

urlpatterns = [
    url('', include(router.urls)),

]