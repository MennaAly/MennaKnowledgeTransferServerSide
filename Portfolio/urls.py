from django.conf.urls import url, include
from rest_framework import routers
from Portfolio.views import ProfileViewSet

router = routers.SimpleRouter()

router.register(r'profile', ProfileViewSet)

urlpatterns = [
    url('', include(router.urls)),

]