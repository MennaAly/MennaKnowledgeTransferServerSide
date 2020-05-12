from rest_framework import viewsets, status
from rest_framework.response import Response

from Blog.models import Post
from Blog.serializers import PostSaveSerializer
from MasterData.models import Tag


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    post_instance = None
    request_data = None
    post_serializer = None

    def get_queryset(self):
        action = self.request.query_params.get('action')
        if action == 'save':
            return Post.objects.only('title', 'content')

    def get_serializer_class(self):
        action = self.request.query_params.get('action')
        if action == 'save':
            return PostSaveSerializer

    def get_request_data(self):
        self.request_data = self.request.data

    def serialize_post_using_save_serializer(self):
        return PostSaveSerializer(data=self.request_data)

    def validate_serializer(self, serializer):
        serializer.is_valid(raise_expection=True)

    def save_serializer(self, serializer):
        return serializer.save()

    def create_post_instance(self):
        self.post_serializer = self.serialize_post_using_save_serializer()
        self.validate_serializer(self.post_serializer)
        self.post_instance = self.save_serializer(self.post_serializer)

    def get_tag_instances(self):
        tag_ids = self.request_data['tag_ids']
        return Tag.objects.filter(id__in=tag_ids)

    def associate_post_with_tags(self):
        tag_instances = self.get_tag_instances()
        self.post_instance.tags.add(*tag_instances)

    def create(self, request, *args, **kwargs):
        self.get_request_data()
        self.create_post_instance()
        self.associate_post_with_tags()
        return Response(status=status.HTTP_200_OK)
