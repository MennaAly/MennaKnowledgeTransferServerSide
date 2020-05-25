from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from Blog.views.post_viewset import PostViewSet

router = routers.SimpleRouter()
router.register(r'post', PostViewSet)

urlpatterns = [
    url('', include(router.urls)),
]
