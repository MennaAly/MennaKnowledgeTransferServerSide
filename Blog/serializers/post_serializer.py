import markdown2
from rest_framework import serializers

from Blog.models import Post

from markdownify import markdownify as md


class PostSaveSerializer(serializers.ModelSerializer):
    # markdown_content = serializers.CharField()

    class Meta:
        model = Post
        fields = [
            'title',
            'markdown_content'
        ]