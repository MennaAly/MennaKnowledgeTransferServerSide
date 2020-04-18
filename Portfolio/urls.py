from django.conf.urls import url, include
from rest_framework import routers
from Portfolio.views import ProfileViewSet, ProjectViewSet
from Portfolio.views.job_viewset import JobViewSet

router = routers.SimpleRouter()

router.register(r'profile', ProfileViewSet)
router.register(r'project',ProjectViewSet)
router.register(r'job',JobViewSet)

urlpatterns = [
    url('', include(router.urls)),

]