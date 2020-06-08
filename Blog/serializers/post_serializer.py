import markdown2
from rest_framework import serializers

from Blog.models import Post

from markdownify import markdownify as md

from MasterData.models import Tag
from MasterData.serializers import TagSerializer


class PostSaveSerializer(serializers.ModelSerializer):
    # markdown_content = serializers.CharField()

    class Meta:
        model = Post
        fields = [
            'title',
            'markdown_content'
        ]


class PostWithTagsSerializer(serializers.ModelSerializer):
    assigned_tags = serializers.SerializerMethodField()

    def get_assigned_tags(self, post_instance):
        tags = Tag.objects.filter(post__id=post_instance.id)
        return TagSerializer(tags, many=True).data

    class Meta:
        model = Post
        fields = [
            'title',
            'markdown_content',
            'assigned_tags',
            'created_date'
        ]
