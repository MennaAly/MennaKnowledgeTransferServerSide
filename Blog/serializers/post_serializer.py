from rest_framework import serializers

from Blog.models import Post

from markdownify import markdownify as md

class PostSaveSerializer(serializers.ModelSerializer):
    content = serializers.CharField()

    class Meta:
        model = Post
        fields = [
            'title',
            'content'
        ]

    def convert_content_from_html_to_markdown(self, validated_data):
        html_content = validated_data.get('content', '')
        return md(html_content)

    def create(self, validated_data):
        markdown_content = self.convert_content_from_html_to_markdown(validated_data)
        return Post.objects.create(title=validated_data.get('title', ''), content=markdown_content)
